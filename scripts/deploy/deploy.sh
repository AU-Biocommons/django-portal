# Deploy to ubuntu server

set -e

CERTBOT_EMAIL=c.hyde@qcif.edu.au
RUN_USER=www-data
RUN_GROUP=www-data
HOSTNAME=django-sandpit.genome.edu.au
APP_DIRNAME=apollo_portal
REPO_DIR=~/apollo_portal
APP_DIR=$REPO_DIR/$APP_DIRNAME
GITHUB_URL=https://github.com/AU-Biocommons/django-portal.git
SQLITE_FILEPATH=/srv/sites/apollo_portal/apollo_portal/db.sqlite3


# Clone repo
git clone $GITHUB_URL $REPO_DIR

# Create venv and install python deps
sudo apt install -y python3-pip
sudo python3 -m pip install virtualenv
virtualenv $REPO_DIR/venv
source $REPO_DIR/venv/bin/activate
pip install -r requirements.txt

# Setup site dir
sudo mkdir /srv/sites
sudo ln -s $APP_DIR /srv/sites/$APP_DIRNAME
sudo chown $RUN_USER:$RUN_GROUP $SQLITE_FILEPATH

# Setup nginx
sudo apt install -y nginx
sudo ln -s $REPO_DIR/scripts/deploy/nginx.conf /etc/nginx/sites-available/$HOSTNAME
sudo ln -s /etc/nginx/sites-available/$HOSTNAME /etc/nginx/sites-enabled/$HOSTNAME
sudo rm /etc/nginx/sites-enabled/default
sudo service nginx restart

# SSL certs
sudo apt install -y python-certbot-nginx
sudo certbot --nginx -d $HOSTNAME --non-interactive --agree-tos --email $CERTBOT_EMAIL

# Setup gunicorn
sudo ln -s $REPO_DIR/scripts/deploy/apollo_portal.service /etc/systemd/system/apollo_portal.service
sudo ln -s $REPO_DIR/scripts/deploy/apollo_portal.socket /etc/systemd/system/apollo_portal.socket
sudo systemctl enable apollo_portal.service
sudo systemctl enable apollo_portal.socket

# Build application
cd $APP_DIR
python manage.py migrate
python manage.py build_index
python manage.py collectstatic --noinput

# Request .env file content
cp $REPO_DIR/.env.sample $REPO_DIR/.env
printf "\nPlease populate $REPO_DIR/.env file before continuing...\n"
read -p "Press enter to continue"

# Start application
sudo systemctl restart apollo_portal.service

echo "Deployment complete."
echo "Please run `python manage.py createsuperuser` to create an admin user."
