#!/bin/bash

echo "Esperando a que la base de datos esté disponible..."
while ! nc -z db 5432; do
  sleep 1
done

echo "Aplicando migraciones con Flask-Migrate..."
flask db upgrade

echo "Levantando servidor Flask..."
exec flask run --host=0.0.0.0