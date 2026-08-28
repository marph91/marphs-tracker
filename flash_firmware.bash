#!/usr/bin/env bash
set -euo pipefail

src="./firmware"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

run=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --run)
            run=true
            shift
            ;;
        *)
            echo "Unknown argument: $1" >&2
            exit 1
            ;;
    esac
done

# Copy firmware to staging directory while applying exclusions.
rsync -a \
    --exclude='__pycache__/' \
    --exclude='.pytest_cache/' \
    --exclude='tests/' \
    --exclude='*.md' \
    "$src/" "$tmp/"

echo "copy:    firmware"

(
    cd "$tmp"
    # One mpremote invocation.
    mpremote fs cp -r . :/
)

if "$run"; then
    echo "run:     main.py"
    mpremote run ./firmware/main.py
fi
