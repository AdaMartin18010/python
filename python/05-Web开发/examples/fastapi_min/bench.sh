#!/usr/bin/env bash
set -euo pipefail

URL=${1:-http://127.0.0.1:8000/health}

echo "== hey (2k req, c100) =="
hey -n 2000 -c 100 "$URL" || echo "hey not installed"

echo "== wrk (t4 c100 d30s) =="
wrk -t4 -c100 -d30s "$URL" || echo "wrk not installed"


