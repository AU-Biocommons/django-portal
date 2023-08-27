# Update to latest commit

set -e

. $(dirname $0)/vars.sh

# Pull changes
sudo su $BUILD_USER
cd $REPO_DIR
git pull

# Build application
cd $APP_DIR
. $VENV_DIR/bin/activate
python manage.py migrate
python manage.py build_index
python manage.py collectstatic --noinput
sudo chown $RUN_USER:$RUN_GROUP $SQLITE_FILEPATH
sudo chown -R $RUN_USER:$RUN_GROUP $STATIC_ROOT

# Start application
sudo systemctl restart apollo_portal.service

echo ""
echo "~~~ Restarted Apollo Portal ~~~"
echo ""
