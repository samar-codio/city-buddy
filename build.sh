#!/usr/bin/env bash
# Render build script — runs on every deploy
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate

# Seed the product offers (idempotent — clears and re-creates)
python manage.py seed_offers
