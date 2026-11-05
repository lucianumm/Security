#!/bin/sh
# Portable fail-closed wrapper. Requires Python 3.9+ and the standard library.
set -eu
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=${1:-.}
if command -v python3 >/dev/null 2>&1; then
  exec python3 "$SCRIPT_DIR/security_auditor.py" gate --root "$ROOT"
fi
if command -v python >/dev/null 2>&1; then
  exec python "$SCRIPT_DIR/security_auditor.py" gate --root "$ROOT"
fi
printf '%s\n' '{"result":"ERROR","reason":"Python 3.9+ is required"}'
exit 2
