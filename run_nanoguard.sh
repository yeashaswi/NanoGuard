#!/bin/bash
# NanoGuard Startup Script
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "=========================================================="
echo "🛡️  NanoGuard: Nanoparticle Pollutant Detection Telemetry"
echo "=========================================================="

# Ensure temporary credentials exist
mkdir -p /tmp/.streamlit
if [ ! -f /tmp/.streamlit/credentials.toml ]; then
    printf '[general]\nemail = ""\n' > /tmp/.streamlit/credentials.toml
fi

echo "Checking test suite..."
HOME=/tmp ./venv/bin/python -m unittest tests/test_model_pipeline.py

echo ""
echo "Starting Minimalist UI at http://localhost:8501 ..."
export HOME=/tmp
./venv/bin/python -m streamlit run app.py --server.headless true --server.port 8501
