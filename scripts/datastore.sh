# Helpers for keeping research datasets in the GitHub release "data".
# Source this file in a workflow step; needs GH_TOKEN and GITHUB_REPOSITORY.
#
# A dataset is a directory under data/ (e.g. data/intraday/5min). It is stored
# as <name>.tar.partNN assets, split at 1.9 GB because GitHub limits each
# release file to 2 GB.

RELEASE=data

ensure_release() {
  gh release view "$RELEASE" >/dev/null 2>&1 || gh release create "$RELEASE" \
    --title "Research data" --latest=false \
    --notes "Datasets maintained by the alpaca-data and fundamentals-data workflows. Each dataset is a tar archive split into .partNN files: cat NAME.tar.part* | tar -x -C data. Manifests: datasets/ on the results branch."
}

# fetch_dataset NAME DIR -> 0 if found and extracted into data/DIR, 1 otherwise
fetch_dataset() {
  local name=$1 dir=$2 tmp=/tmp/fetch_$1
  [ -d "data/$dir" ] && ls "data/$dir"/* >/dev/null 2>&1 && return 0   # already here
  rm -rf "$tmp"; mkdir -p "$tmp" data
  if gh release download "$RELEASE" --pattern "$name.tar.part*" --dir "$tmp" 2>/dev/null \
     && ls "$tmp"/"$name".tar.part* >/dev/null 2>&1; then
    cat $(ls "$tmp"/"$name".tar.part* | sort) | tar -x -C data
    echo "fetched $name ($(du -sh "data/$dir" | cut -f1))"; rm -rf "$tmp"; return 0
  fi
  # one-time migration of the first 5-minute download (old release "intraday-data")
  if [ "$name" = intraday_5min ] && gh release download intraday-data --pattern intraday_5min.tar --dir "$tmp" 2>/dev/null; then
    mkdir -p data/intraday && tar -xf "$tmp/intraday_5min.tar" -C data/intraday
    echo "fetched $name from the old intraday-data release"; rm -rf "$tmp"; return 0
  fi
  rm -rf "$tmp"; return 1
}

# save_dataset NAME DIR: archive data/DIR and replace the release assets
save_dataset() {
  local name=$1 dir=$2 out=/tmp/save_$1
  [ -d "data/$dir" ] || return 0
  ensure_release
  rm -rf "$out"; mkdir -p "$out"
  tar -C data -cf - "$dir" | split -b 1900m -d -a 2 - "$out/$name.tar.part"
  ls -lh "$out"
  gh release upload "$RELEASE" "$out"/* --clobber
  # delete parts left over from a bigger previous archive
  local keep; keep=$(cd "$out" && ls)
  for asset in $(gh release view "$RELEASE" --json assets -q '.assets[].name' | grep "^$name\.tar\.part"); do
    echo "$keep" | grep -qx "$asset" || gh release delete-asset "$RELEASE" "$asset" --yes
  done
  rm -rf "$out"
  # the old single-file release is no longer needed once the 5-minute data is saved here
  if [ "$name" = intraday_5min ] && gh release view intraday-data >/dev/null 2>&1; then
    gh release delete intraday-data --yes --cleanup-tag || true
  fi
}

# publish_manifest NAME DIR: copy manifest files to datasets/NAME on the results branch
publish_manifest() {
  local name=$1 dir=$2 res
  [ -f "data/$dir/manifest.json" ] || return 0
  git config --global user.name "github-actions[bot]"
  git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"
  res=$(mktemp -d)
  for attempt in 1 2 3 4 5; do
    rm -rf "$res"; mkdir -p "$res"
    (
      cd "$res" && git init -q
      git remote add origin "https://x-access-token:${GH_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
      if git fetch -q --depth 1 origin results; then git checkout -q -B results FETCH_HEAD; else git checkout -q --orphan results; fi
      mkdir -p "datasets/$name"
      for f in manifest.json manifest.csv symbols.csv; do
        [ -f "$GITHUB_WORKSPACE/data/$dir/$f" ] && cp "$GITHUB_WORKSPACE/data/$dir/$f" "datasets/$name/"
      done
      [ "$name" = intraday_5min ] && [ -d intraday ] && git rm -rq intraday
      git add -A
      git commit -q -m "Dataset manifest: $name (run ${GITHUB_RUN_ID})" || exit 0
      git push -q origin results
    ) && break
    sleep $((attempt * 15))
  done
  rm -rf "$res"
  { echo "### $name"; echo '```json'; cat "data/$dir/manifest.json"; echo '```'; } >> "$GITHUB_STEP_SUMMARY"
}

dataset_complete() {
  python -c "import json,sys; sys.exit(0 if json.load(open('data/$1/manifest.json')).get('complete', True) else 1)"
}
