"""The clock dispatches each job once per slot, in the job's own time zone, weekdays only where set."""
import pandas as pd

from qtrade import clock as C


def _job(name):
    return next(j for j in C.JOBS if j.workflow == name)


def test_flip_due_after_1545_new_york_on_weekdays_only():
    j = _job("flip-sleeve.yml")
    mon = pd.Timestamp("2026-10-26 19:50", tz="UTC")             # 15:50 New York (summer time)
    assert C.due(j, mon) == ["flip-sleeve.yml|{}|2026-10-26 15:45"]
    assert C.due(j, pd.Timestamp("2026-10-26 19:40", tz="UTC")) == []          # 15:40: not yet
    assert C.due(j, pd.Timestamp("2026-10-31 19:50", tz="UTC")) == []          # Saturday


def test_hoard_every_30_minutes_and_archive_jobs_are_distinct():
    h = _job("data-hoard.yml")
    assert C.due(h, pd.Timestamp("2026-10-25 10:10", tz="UTC")) == ["data-hoard.yml|{}|2026-10-25 10:07"]
    keys = [k for j in C.JOBS if j.workflow == "hoard-archive.yml"
            for k in C.due(j, pd.Timestamp("2026-10-26 20:50", tz="UTC"))]   # 16:50 New York
    assert keys == ["hoard-archive.yml|{'job': 'eod'}|2026-10-26 16:45"]


def test_run_fires_each_slot_once(monkeypatch):
    times = iter([pd.Timestamp("2026-10-26 17:16", tz="UTC"), pd.Timestamp("2026-10-26 17:17", tz="UTC")])
    clock = {"t": 0.0}
    monkeypatch.setattr(C.pd.Timestamp, "now", staticmethod(lambda tz=None: next(times)))
    monkeypatch.setattr(C.time, "time", lambda: clock["t"])
    monkeypatch.setattr(C.time, "sleep", lambda s: clock.__setitem__("t", clock["t"] + 1800))
    fired = C.run(1.0, "o/r", "main", dry_run=True)       # polls at 0 s and 1800 s, both within the 17:15 slot
    assert sum("foreign-sheet.yml" in f for f in fired) == 1
