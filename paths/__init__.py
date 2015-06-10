from . import html, api

ROUTES = (
    #API urls
    (["GET"], "/catalog.json", api.catalog_json),
    (["GET"], "/catalog.xml", api.catalog_xml),
    (["GET"], "/categories.json", api.categories_json),
    (["GET"], "/categories.xml", api.categories_xml),
    (["GET"], "/items.json", api.items_json),
    (["GET"], "/items.xml", api.items_xml),


    #HTML urls
    #session urls
    (["GET"], "/logout", html.logout),
    (["POST"], "/gconnect", html.gconnect),
    (["POST"], "/fbconnect", html.fbconnect),

    (["GET"], "/", html.home),
    (["GET"], "/error", html.error),
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

)
