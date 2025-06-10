#!/bin/sh
echo "→ Aplicando migraciones..."
flask db upgrade
echo "→ Iniciando la aplicación"
python run.py