# Apollo Portal

Apollo portal with the Django web framework

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
list could be replaced with a sitemap.xml in future.
