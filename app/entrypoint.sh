#!/bin/sh

python manage.py wait_for_db
python manage.py migrate
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); username='admin'; password='dörtmevsim35AA'; email='admin@example.com'; User.objects.filter(username=username).exists() or User.objects.create_superuser(username, email, password)"
python manage.py runserver 0.0.0.0:8000