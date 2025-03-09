#!/bin/bash
set -o errexit

# Создаем директорию для SQLite
mkdir -p /var/lib/render/instance

# Устанавливаем зависимости
pip install -r requirements.txt

python -m flask db upgrade

sqlite3 old.db .dump > dump.sql

sed -i 's/INTEGER PRIMARY KEY AUTOINCREMENT/SERIAL PRIMARY KEY/g' dump.sql
sed -i 's/DATETIME/TIMESTAMP/g' dump.sql

PGPASSWORD=yourpass psql -h host -U user -d dbname -f dump.sql
