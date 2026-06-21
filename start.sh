#!/usr/bin/env bash
set -euo pipefail

# Start script for Railway/Heroku-style platforms.
# It runs migrations, collectstatic, seeds offers, then starts Gunicorn.

python3 manage.py collectstatic --noinput
python3 manage.py migrate --noinput
# Seed offers; ignore failures to keep deploy idempotent
python3 manage.py seed_offers || true

exec gunicorn citybuddy.wsgi:application --bind 0.0.0.0:${PORT:-8000}
