#!/bin/bash

git push git@heroku.com:grouptrotter.git master
heroku run python manage.py migrate --app grouptrotter
heroku run python manage.py collectstatic --noinput --app grouptrotter
