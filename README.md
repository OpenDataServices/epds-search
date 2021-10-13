# Install dependencies in a python virtualenv

```
$ setup.sh
```

# Dokku

```
 dokku apps:create epds-search
 dokku config:set epds-search ALLOWED_HOSTS=<hostname>
 dokku plugin:install https://github.com/dokku/dokku*elasticsearch.git elasticsearch
 dokku plugin:install https://github.com/dokku/dokku*postgres.git postgres
 dokku postgres:create epdssearch_db
 dokku postgres:link epdssearch_db epds-search
 dokku elasticsearch:create epdssearch_idx
 dokku elasticsearch:link epdssearch_idx epds-search
 dokku domains:add epds-search <domainname>
 dokku config:set epds-search ES_HOST=172.17.0.3:9200
 dokku run epds-search ./app/manage.py search_index --create
 dokku run epds-search ./app/manage.py load_data postgresql://<user>:<pass>@<host>/epds

 # collect static files for project
 dokku run epds-search ./app/manage.py collectstatic -v 3 --noinput
 # mount the django static files directory
 dokku docker-options:add epds-search deploy "-v /home/dokku/epds-search/static:/app/app/static/"

 # Setup nginx to serve up static files
 mkdir /home/dokku/epds-search/nginx.conf.d/
 echo "location /static {
    autoindex off;
    alias   /home/dokku/epds-search/static;
 }" >> /home/dokku/epds-search/nginx.conf.d/static.conf

 service nginx reload
```

# Map application in app/ui/static/map/

The map search application is a node 14 built app.

https://github.com/OpenDataServices/epds/tree/main/map

To update the application:

```
$ git clone https://github.com/OpenDataServices/epds.git
$ cd epds/map/
$ GEOSERVER_HOST=<hostname of geoserver> npm run  build -- --dist-dir=../../epds-search/app/ui/static/mapp
```