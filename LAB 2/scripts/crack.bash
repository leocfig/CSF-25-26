#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<EOF
Usage: $0 [-w wordlist] [-g glob_pattern]
Defaults:
  wordlist: ./passwords.txt
  glob:     ./*.zip

Examples:
  $0 -w mypwlist.txt -g './archives/*.zip'
  $0 -g '*.zip'
Output:
  /path/to/archive.zip:password
  /path/to/archive.zip:NOT-FOUND
Notes:
  - Loads the whole wordlist into memory (for small lists).
  - Uses 'unzip -t -P <pw>' (no extraction). 'unzip -P' is visible in process list while running.
EOF
}

wordlist="./passwords.txt"
globpattern="./*.zip"

while getopts ":w:g:h" opt; do
  case "$opt" in
    w) wordlist="$OPTARG" ;;
    g) globpattern="$OPTARG" ;;
    h) usage; exit 0 ;;
    *) usage; exit 2 ;;
  esac
done

if [ ! -f "$wordlist" ]; then
  echo "Wordlist not found: $wordlist" >&2
  exit 2
fi
if ! command -v unzip >/dev/null 2>&1; then
  echo "unzip not installed or not in PATH" >&2
  exit 2
fi

# Read whole wordlist into array (preserves whitespace in lines)
mapfile -t pwds < "$wordlist"

# Expand globpattern into array `zips`
# WARNING: don't pass untrusted text as globpattern (uses eval).
eval "zips=( $globpattern )"

if [ "${#zips[@]}" -eq 0 ]; then
  echo "No zip files matched pattern: $globpattern" >&2
  exit 0
fi

for zip in "${zips[@]}"; do
  # ensure it's a regular file
  if [ ! -f "$zip" ]; then
    printf '%s:NOT-FOUND\n' "$zip"
    continue
  fi

  found_pw=""
  for pw in "${pwds[@]}"; do
    # skip empty lines
    [ -z "$pw" ] && continue
    if unzip -P"$pw" -qq -t -- "$zip" >/dev/null 2>&1; then
      found_pw="$pw"
      break
    fi
  done

  if [ -n "$found_pw" ]; then
    printf '%s:%s\n' "$zip" "$found_pw"
  else
    printf '%s:NOT-FOUND\n' "$zip"
  fi
done

