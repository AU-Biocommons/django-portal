# Vars for running scripts

CERTBOT_EMAIL=c.hyde@qcif.edu.au
BUILD_USER=c.hyde
RUN_USER=www-data
RUN_GROUP=www-data
HOSTNAME=django-sandpit.genome.edu.au
APP_DIRNAME=apollo_portal
REPO_DIR=/srv/sites/apollo_portal
APP_DIR=$REPO_DIR/$APP_DIRNAME
VENV_DIR=$REPO_DIR/venv
STATIC_ROOT=$APP_DIR/apollo_portal/static
GITHUB_URL=https://github.com/AU-Biocommons/django-portal.git
SQLITE_FILEPATH=$APP_DIR/db.sqlite3
DJANGO_SETTINGS_MODULE=apollo_portal.settings.prod
