Catalog with items and their categories
=======================================

This creates an app through wich you can list with items and their categories.

With right credentials you can `add`, `edit`, `delete` items / categories / descriptions.


## Before starting the app

Before starting the app 2 files shoud be created in `config` folder

`google.json` should be the json file from google
```json
{
    "web": {
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "client_secret": "CLIENT SECRET",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "client_email": "CLIENT EMAIL",
        "redirect_uris": ["https://www.example.com/oauth2callback"],
        "client_x509_cert_url": "CERT URL",
        "client_id": "CLIENT ID",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "javascript_origins": ["https://www.example.com","http://localhost:5000"]
    }
}
```
`facebook.json` should contain `id` and `secret` keys from facebook
```json
{
    "id": "CLIENT ID",
    "secret": "SECRET KEY"
}
```


## Available `make` targets:
* `configure` sets up the inviroment, installs all dependencies
* `make db` sets up the db
* `make fulldb` creates(if not already exists) and populates db
* `make server` runs the app, navigate to localhost:5000 to access the project


## List of all urls

#### API urls
* `/catalog.json` GET
* `/catalog.xml` GET
* `/categories.json` GET
* `/categories.xml` GET
* `/items.json` GET
* `/items.xml` GET

#### HTML urls
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
