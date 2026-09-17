#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Automatically ensure superuser exists with staff and superuser permissions
python manage.py shell << 'EOF'
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.getenv("DJANGO_SUPERUSER_USERNAME")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD")
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@vegeview.com")

if username and password:
    user = User.objects.filter(username=username).first()
    if not user and email:
        user = User.objects.filter(email=email).first()

    if not user:
        user = User.objects.create_user(username=username, email=email)
        print(f"Created new superuser: {username}")
    else:
        user.username = username
        print(f"Updating existing superuser: {username}")

    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()
    print(f"Superuser '{username}' successfully configured with staff and admin access.")
else:
    print("DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD not set; skipping superuser creation.")
EOF
