#!/usr/bin/env bash
set -e
echo "[run_checks] running pylint..."
if ! command -v pylint >/dev/null 2>&1; then
  echo "pylint missing. Install with: pip install pylint"
  exit 1
fi
pylint modules/*.py || true
echo "[run_checks] generating SBOM..."
python -c "import slsa_generator; slsa_generator.generate_sbom('sbom.json')"
echo "[run_checks] done."