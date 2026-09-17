#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Automatically create superuser if environment variables are set
if [[ -n "" && -n "" ]]; then
  echo "Ensuring superuser exists..."
  python manage.py createsuperuser --no-input || true
fi
