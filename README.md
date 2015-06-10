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
* /catalog.json `GET`
* /catalog.xml `GET`
* /categories.json `GET`
    (["GET"], "/categories.xml", api.categories_xml),
    (["GET"], "/items.json", api.items_json),
    (["GET"], "/items.xml", api.items_xml),


    #HTML urls
    #session urls
    (["GET"], "/logout", html.logout),
    (["POST"], "/gconnect", html.gconnect),
    (["POST"], "/fbconnect", html.fbconnect),

    (["GET"], "/", html.home),
    #category urls
    (["GET"], "/category/<int:category_id>/", html.category),
    (["GET", "POST"], "/category/create/", html.create_category),
    (["GET", "POST"], "/category/<int:category_id>/edit/", html.edit_category),
    (["GET", "POST"], "/category/<int:category_id>/delete/", html.delete_category),
    #item urls
    (["GET"], "/item/<int:item_id>/", html.item),
    (["GET", "POST"], "/item/create/", html.create_item),
    (["GET", "POST"], "/item/<int:item_id>/edit/", html.edit_item),
    (["GET", "POST"], "/item/<int:item_id>/delete/", html.delete_item),
