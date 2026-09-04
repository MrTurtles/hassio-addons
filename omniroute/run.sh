#!/bin/sh
set -e

INITIAL_PASSWORD=$(node -e "console.log(require('/data/options.json').initial_password)")

export INITIAL_PASSWORD
export PORT="20128"
export DASHBOARD_PORT="20128"
export API_HOST="0.0.0.0"
export DATA_DIR="/data"

echo "Starting OmniRoute..."
exec omniroute
