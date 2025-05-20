#!/usr/bin/env bash

set -o errexit

cd RecetaPag  # Entra a la carpeta que contiene manage.py
pip install -r ../requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
