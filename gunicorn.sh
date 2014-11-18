#!/bin/sh
PROJECT_PATH=/home/odoo/finance
export PYTHONPATH=$PROJECT_PATH:$PYTHONPATH
NAME="EnergyConservation"                                  # Name of the application
NUM_WORKERS=3                                               # how many worker processes should Gunicorn spawn
BIND="127.0.0.1:8888"
DJANGO_SETTINGS_MODULE=taskmanagement.settings            # which settings file should Django use
DJANGO_WSGI_MODULE=taskmanagement.wsgi                     # WSGI module name


# Activate the virtual environment
cd $PROJECT_PATH
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --bind=$BIND \
  --reload \
  --log-level=debug \
  --access-logfile /home/odoo/logs/access.log \
  --error-logfile /home/odoo/logs/error.log
#exec gunicorn -c /home/odoo/finance/gunicorndebug.py --log-level=debug taskmanagement.wsgi:application