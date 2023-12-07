#!/bin/sh

if [ "$SQL_ENGINE" = "django.db.backends.postgresql" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.5
    done

    echo "✓ PostgreSQL started"
fi

set -e

echo -e "\e[46m$(python -V)\e[0m"
echo -e "which python: \033[0;34m$(which python)"


# python manage.py flush --no-input
python manage.py migrate

exec "$@"
