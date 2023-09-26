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
python manage.py collectstatic --noinput
python manage.py build_index
sudo chown $BUILD_USER:$RUN_GROUP $SQLITE_FILEPATH
sudo chown $BUILD_USER:$RUN_GROUP $SQLITE_DIR
sudo chmod 664 $SQLITE_FILEPATH
sudo chmod 775 $SQLITE_DIR

# Start application
sudo systemctl restart apollo_portal.service

echo ""
echo "~~~ Restarted Apollo Portal ~~~"
echo ""
