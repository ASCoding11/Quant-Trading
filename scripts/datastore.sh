# Helpers for keeping research datasets in the GitHub release "data".
# Source this file in a workflow step; needs GH_TOKEN, GITHUB_REPOSITORY and
# DATA_KEY (a repository secret).
#
# A dataset is a directory under data/ (e.g. data/intraday/5min). It is stored
# ENCRYPTED (AES-256, key = DATA_KEY) as <name>.tar.enc.partNN assets, split at
# 1.9 GB because GitHub limits each release file to 2 GB. The repository is
# public, and market data and news are licensed for personal use only, so they
# are never uploaded unencrypted.
#
# To unpack a dataset on your own computer:
#   cat NAME.tar.enc.part* | openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -pass env:DATA_KEY | tar -x -C data

RELEASE=data
ENC_ARGS="-aes-256-cbc -pbkdf2 -iter 200000 -pass env:DATA_KEY"

require_key() {
  if [ -z "${DATA_KEY:-}" ]; then
    echo "::error::Add a DATA_KEY repository secret (any long random password) - datasets are stored encrypted."
    exit 1
  fi
}

ensure_release() {
  gh release view "$RELEASE" >/dev/null 2>&1 || gh release create "$RELEASE" \
    --title "Research data (encrypted)" --latest=false \
    --notes "Encrypted datasets maintained by this repository's workflows (licensed for the owner's personal research use only). Manifests describing them: datasets/ on the results branch."
}

# fetch_dataset NAME DIR -> 0 if found and extracted into data/DIR, 1 otherwise
fetch_dataset() {
  local name=$1 dir=$2 tmp=/tmp/fetch_$1
  [ -d "data/$dir" ] && ls "data/$dir"/* >/dev/null 2>&1 && return 0   # already here
  rm -rf "$tmp"; mkdir -p "$tmp" data
  if gh release download "$RELEASE" --pattern "$name.tar.enc.part*" --dir "$tmp" 2>/dev/null \
     && ls "$tmp"/"$name".tar.enc.part* >/dev/null 2>&1; then
    require_key
    if ! (set -o pipefail; cat $(ls "$tmp"/"$name".tar.enc.part* | sort) | openssl enc -d $ENC_ARGS | tar -x -C data); then
      echo "::error::Could not decrypt $name - DATA_KEY does not match the key it was saved with."
      exit 1
    fi
    echo "fetched $name ($(du -sh "data/$dir" | cut -f1))"; rm -rf "$tmp"; return 0
  fi
  # older unencrypted copies (before the repository became public)
  if gh release download "$RELEASE" --pattern "$name.tar.part*" --dir "$tmp" 2>/dev/null \
     && ls "$tmp"/"$name".tar.part* >/dev/null 2>&1; then
    cat $(ls "$tmp"/"$name".tar.part* | sort) | tar -x -C data
    echo "fetched unencrypted $name ($(du -sh "data/$dir" | cut -f1))"; rm -rf "$tmp"; return 0
  fi
  rm -rf "$tmp"; return 1
}

# save_dataset NAME DIR: encrypt data/DIR and replace the release assets
save_dataset() {
  local name=$1 dir=$2 out=/tmp/save_$1
  [ -d "data/$dir" ] || return 0
  require_key
  ensure_release
  rm -rf "$out"; mkdir -p "$out"
  (set -o pipefail; tar -C data -cf - "$dir" | openssl enc -e $ENC_ARGS | split -b 1900m -d -a 2 - "$out/$name.tar.enc.part") \
    || { echo "::error::Could not archive $name"; exit 1; }
  ls -lh "$out"
  gh release upload "$RELEASE" "$out"/* --clobber
  # remove leftover encrypted parts and every unencrypted part of this dataset
  local keep; keep=$(cd "$out" && ls)
  for asset in $(gh release view "$RELEASE" --json assets -q '.assets[].name' | grep -E "^$name\.tar\.(enc\.)?part"); do
    echo "$keep" | grep -qx "$asset" || gh release delete-asset "$RELEASE" "$asset" --yes
  done
  rm -rf "$out"
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
      # (this used to delete intraday/ whenever the 5-minute dataset changed, which also removed the
      # auction trader's universe and directions - intraday/latest/model.json, intraday/edge/signs.json)
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
