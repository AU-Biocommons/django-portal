# Deploy to ubuntu server

set -e

. $(dirname $0)/vars.sh

sudo su $BUILD_USER

# Clone repo
git clone $GITHUB_URL $REPO_DIR

# Create venv and install python deps
sudo apt install -y python3-pip
sudo python3 -m pip install virtualenv
virtualenv $VENV_DIR
source $VENV_DIR/bin/activate
pip install -r $REPO_DIR/requirements.txt
echo "export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE" >> $VENV_DIR/bin/activate

# Setup nginx
sudo apt install -y nginx
sudo ln -s $REPO_DIR/deploy/nginx.conf /etc/nginx/sites-available/$HOSTNAME
sudo ln -s /etc/nginx/sites-available/$HOSTNAME /etc/nginx/sites-enabled/$HOSTNAME
sudo rm /etc/nginx/sites-enabled/default
sudo service nginx restart

# SSL certs
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d $HOSTNAME --non-interactive --agree-tos --email $CERTBOT_EMAIL

# Setup gunicorn
sudo ln -s $REPO_DIR/deploy/apollo_portal.service /etc/systemd/system/apollo_portal.service
sudo ln -s $REPO_DIR/deploy/apollo_portal.socket /etc/systemd/system/apollo_portal.socket
sudo systemctl enable apollo_portal.service
sudo systemctl enable apollo_portal.socket

# Request .env file content
cp $REPO_DIR/.env.sample $REPO_DIR/.env
printf "\nPlease populate $REPO_DIR/.env file before continuing...\n"
read -p "Press enter to continue > "

# Build application
cd $APP_DIR
python manage.py migrate
python manage.py build_index
python manage.py collectstatic --noinput
sudo chmod 775 $SQLITE_FILEPATH
sudo chown $BUILD_USER:$RUN_GROUP $SQLITE_FILEPATH
sudo chown -R $RUN_USER:$RUN_GROUP $STATIC_ROOT
sudo usermod -a -G $RUN_GROUP $BUILD_USER

# Start application
sudo systemctl restart apollo_portal.service

echo "Deployment complete."
echo "Please run `python manage.py createsuperuser` to create an admin user."
