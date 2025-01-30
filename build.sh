#!/usr/bin/env bash

# Загружаем переменные окружения из .env
set -o allexport
source .env
set +o allexport

# Запускаем psql
psql -a "$DATABASE_URL" -f init.sql
