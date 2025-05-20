#!/usr/bin/env bash

set -o errexit  # Detiene el script si hay algún error

pip install -r requirements.txt  # Instala las dependencias desde la raíz del proyecto

python manage.py collectstatic --no-input  # Recolecta archivos estáticos para producción
python manage.py migrate  # Aplica migraciones
