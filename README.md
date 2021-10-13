# Install dependencies in a python virtualenv

```
$ setup.sh
```


# Dokku

# Map application in static/map/

The map search application is a node 14 built app.

https://github.com/OpenDataServices/epds/tree/main/map


```
$ git clone https://github.com/OpenDataServices/epds.git
$ cd epds/map/
$ GEOSERVER_HOST=<hostname of geoserver> npm run  build -- --dist-dir=../../epds-search/app/ui/static/mapp
```