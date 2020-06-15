#!/bin/bash

# run db migrations
python ./manage.py migrate --no-input

# copy static files
python ./manage.py collectstatic --no-input

echo "Init is done!"

# launch parameters
exec ${@}
