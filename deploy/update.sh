#/usr/bin/env bash

set -e

. $(dirname $0)/vars.sh

# Exit if user is not build user:
if [ "$USER" != "$BUILD_USER" ]; then
    echo "ERROR: Must be run as $BUILD_USER"
    exit 1
fi

# Pull changes
cd $REPO_DIR
git pull

# Build application
cd $APP_DIR
. $VENV_DIR/bin/activate
python manage.py migrate
python manage.py build_index
python manage.py collectstatic --noinput
sudo chown $RUN_USER:$RUN_GROUP $SQLITE_FILEPATH

# Start application
sudo systemctl restart apollo_portal.service

echo ""
echo "~~~ Restarted Apollo Portal ~~~"
echo ""
