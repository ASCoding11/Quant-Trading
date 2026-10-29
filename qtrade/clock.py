"""The clock: starts the daily jobs at the right minute instead of trusting GitHub's scheduler.

GitHub starts scheduled workflows late or not at all on busy days (on 2026-10-26 none of the
sleeves' schedules fired). Like the auction keeper, a clock run stays up for ~5.5 hours, polls the
time every 30 seconds and dispatches each job once per slot (``JOBS``); before it ends, the
workflow starts the next clock, so one is always running. Every job is itself idempotent (a sleeve
skips a day it already booked), so a duplicate dispatch does nothing.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import time
from dataclasses import dataclass

import pandas as pd

from .utils import LOG, setup_logging

NY = "America/New_York"


@dataclass(frozen=True)
class Job:
    workflow: str
    tz: str                      # the clock the times are in
    times: tuple                 # "HH:MM" - dispatch once at (or soon after) each
    weekdays: bool = True        # Monday-Friday only
    inputs: tuple = ()           # (key, value) pairs for workflow_dispatch
    window_min: int = 25         # still dispatch if the clock was down at the exact minute


JOBS = [
    Job("data-hoard.yml", "UTC", tuple(f"{h:02d}:{m:02d}" for h in range(24) for m in (7, 37)), weekdays=False,
        window_min=20),
    Job("hft-shadow.yml", NY, ("09:26",), window_min=300),         # its own chain then runs the session
    Job("flip-sleeve.yml", NY, ("15:45",), window_min=400),
    Job("auction-sheet.yml", NY, ("16:30",), window_min=400),
    Job("hoard-archive.yml", NY, ("16:45",), inputs=(("job", "eod"),), window_min=400),
    Job("foreign-sheet.yml", "UTC", ("17:15", "23:30"), window_min=200),   # 23:30: Asian bars Yahoo posted late
    Job("hoard-archive.yml", "UTC", ("07:15",), weekdays=False, inputs=(("job", "archive"),), window_min=300),
]


def due(job: Job, now_utc: pd.Timestamp) -> list[str]:
    """Slot keys (date + time in the job's clock) that are due at ``now_utc``."""
    now = now_utc.tz_convert(job.tz)
    if job.weekdays and now.weekday() >= 5:
        return []
    out = []
    for hhmm in job.times:
        h, m = map(int, hhmm.split(":"))
        at = now.normalize() + pd.Timedelta(hours=h, minutes=m)
        if at <= now < at + pd.Timedelta(minutes=job.window_min):
            out.append(f"{job.workflow}|{dict(job.inputs)}|{at:%Y-%m-%d %H:%M}")
    return out


def dispatch(job: Job, repo: str, ref: str) -> bool:
    cmd = ["gh", "workflow", "run", job.workflow, "-R", repo, "--ref", ref]
    for k, v in job.inputs:
        cmd += ["-f", f"{k}={v}"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        LOG.warning("dispatch %s failed: %s", job.workflow, r.stderr.strip()[:200])
    return r.returncode == 0


def run(hours: float, repo: str, ref: str, dry_run: bool = False) -> list[str]:
    end = time.time() + hours * 3600
    done: set[str] = set()
    fired = []
    while time.time() < end:
        now = pd.Timestamp.now(tz="UTC")
        for job in JOBS:
            for key in due(job, now):
                if key in done:
                    continue
                done.add(key)
                ok = True if dry_run else dispatch(job, repo, ref)
                fired.append(f"{now:%H:%M}Z {key} {'ok' if ok else 'FAILED'}")
                LOG.info("clock: %s", fired[-1])
        time.sleep(30)
    return fired


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=float, default=5.5)
    ap.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", "ASCoding11/Quant-Trading"))
    ap.add_argument("--ref", default="main")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    setup_logging()
    fired = run(args.hours, args.repo, args.ref, args.dry_run)
    print("\n".join(fired) or "nothing due in this window")


if __name__ == "__main__":
    main()
