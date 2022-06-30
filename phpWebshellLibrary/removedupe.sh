#!/bin/bash
declare -A arr
shopt -s globstar

for file in **; do
  [[ -f "$file" ]] || continue

  read cksm _ < <(md5sum "$file")
  if ((arr[$cksm]++)); then
    rm "$file"
    echo "removing dupe $file"
  fi
done
