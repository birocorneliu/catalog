import os
import json
from database_setup import User, Category, Item

PATH = os.path.realpath('.')
dummy_items = json.load(open("{}/lib/dummy_items.json".format(PATH)))


user = User.findone(email="corneliu.biro@gmail.com")
if not user:
    user = User(name="Biro Corneliu", email="corneliu.biro@gmail.com").create()

for categ in dummy_items:
    category = Category.findone(name=categ["name"])
    if not category:
        category = Category(name=categ["name"],
                            picture=categ["picture"],
                            user_id=user.id).create()
    for item in categ["items"]:
        if not Item.findone(name=item["name"], category_id=category.id):
            Item(user_id=user.id, category_id=category.id, **item).create()
