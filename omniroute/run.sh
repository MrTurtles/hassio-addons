#!/usr/bin/with-contenv bashio

INITIAL_PASSWORD=$(bashio::config 'initial_password')

export INITIAL_PASSWORD
export PORT="20128"
export DASHBOARD_PORT="20128"
export API_HOST="0.0.0.0"
export DATA_DIR="/data"

bashio::log.info "Starting OmniRoute..."

exec omniroute
