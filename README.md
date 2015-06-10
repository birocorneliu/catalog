Catalog with items and their categories
=======================================

This creates an app through wich you can list with items and their categories.

With right credentials you can `add`, `edit`, `delete` items / categories / descriptions.

## Available `make` targets:

* `configure` sets up the inviroment, installs all dependencies
* `make db` sets up the db
* `make fulldb` creates(if not already exists) and populates db
* `make server` runs the app, navigate to localhost:5000 to access the project

## List of all urls
* `/catalog.json` GET
* `/catalog.xml` GET
* `/categories.json` GET
* `/categories.xml` GET
* `/items.json` GET
* `/items.xml` GET

### HTML urls
* `/` GET
* `/logout` GET
* `/gconnect` POST
* `/fbconnect` POST
* `/category/<int:category_id>` GET
* `/category/create` GET, POST
* `/category/<int:category_id>/edit` GET, POST
* `/category/<int:category_id>/delete` GET, POST
* `/item/<int:item_id>` GET
* `/item/create/` GET, POST
* `/item/<int:item_id>/edit` GET, POST
* `/item/<int:item_id>/delete` GET, POST
