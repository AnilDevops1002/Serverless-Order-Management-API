#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

export TELEMETRY_ENABLED=false

echo "=== Running automated tests ==="
python -m pytest tests/ -v --cov=src --cov-report=term-missing

echo "=== Checking dependency vulnerabilities ==="
python -m pip_audit -r requirements.txt

echo "=== Building Lambda package ==="
./scripts/package-lambda.sh

echo "=== Validating Lambda ZIP ==="
unzip -t build/lambda.zip >/dev/null

echo "=== Validating Terraform ==="
terraform -chdir=terraform fmt -check
terraform -chdir=terraform validate

echo "=== All verification checks passed ==="
