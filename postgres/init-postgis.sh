#!/bin/bash
if command -v postgis &>/dev/null; then
    psql -U "$POSTGRES_USER" -d template1 -c "CREATE EXTENSION IF NOT EXISTS postgis;"
fi
