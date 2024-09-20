#!/usr/bin/env bash
set -o errexit

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing requirements..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input >> build.log 2>&1

echo "Running migrations..."
python manage.py migrate >> build.log 2>&1

echo "Creating superuser..."
python manage.py createsuperuser >> build.log 2>&1
