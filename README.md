# Apollo Portal

Apollo portal built on the Django web framework.


## Updating the webserver

Updates should be applied through GitHub Workflows on pushes to branches `dev`
and `master`.

An admin can manually update the webserver like so:

```bash
# Assumes you have SSH'd into the webserver
cd $APOLLO_PORTAL_ROOT
deploy/update.sh
```

## Local development setup

Set up and activate a [new virtual environment](https://virtualenv.pypa.io/),
with `python>=3.10`, then do this:

```bash
cd $YOUR_CHOSEN_DIRECTORY
git clone $GIT_REPO_URL apollo_portal
cd apollo_portal
python -m pip install -r requirements
# Jump into the Django project root
cd app
# Set up the database
python manage.py migrate
# Populate the DB with fake data
python manage.py seed
# Build the search index
python manage.py build_index
# Run a development server and check out the application
python manage.py runserver
```


## The search backend

The site search functionality uses the Python Whoosh library. A search index
must be built with every update that changes HTML templates:

```sh
python manage.py build_index
```

This command runs a development server, and makes a requests against it for
every URL in `settings.SITE_SEARCH_URLS`. If a developer updates any URL paths
in the application, they should ensure this list is also updated. i.e. if you
add an endpoint which should be indexed, then add the URL to this list. This
list could be replaced with a `sitemap.xml` file in future.
