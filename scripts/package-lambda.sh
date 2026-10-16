#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

rm -rf build/package build/lambda.zip
mkdir -p build/package

python -m pip install \
  --platform manylinux2014_x86_64 \
  --implementation cp \
  --python-version 3.13 \
  --only-binary=:all: \
  --target build/package \
  -r requirements.txt

cp -r src build/package/

find build/package -type f \( -name "*.bak" -o -name "*.pyc" \) -delete
find build/package -type d -name "__pycache__" -prune -exec rm -rf {} +


cd build/package
zip -qr ../lambda.zip .

echo "Lambda package created successfully"
