#!/bin/bash
set -o errexit

# 1. Установка зависимостей
pip install -r requirements.txt

# 2. Применение миграций структуры БД
python -m flask db upgrade

# 3. Экспорт данных из SQLite
sqlite3 old.db .dump > dump.sql

# 4. Конвертация для PostgreSQL
sed -i \
  -e 's/INTEGER PRIMARY KEY AUTOINCREMENT/SERIAL PRIMARY KEY/g' \
  -e 's/DATETIME/TIMESTAMP/g' \
  -e 's/BLOB/BYTEA/g' \
  -e 's/BLOB/BYTEA/gI' \  # На случай разных регистров
  dump.sql

# 5. Импорт в PostgreSQL (используйте свои параметры)
export PGPASSWORD='1hhFW6tstY4wJwSNmqAtbvMTo8xlyzdk'
psql \
  -h dpg-cv6mnkan91rc73bglbbg-a.oregon-postgres.render.com \
  -U data_8uxi_user \
  -d data_8uxi \
  -p 5432 \
  -f dump.sql

# 6. Очистка
rm dump.sql