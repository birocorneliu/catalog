from lib.database_setup import Item
import json

def home():
    return json.dumps([i.to_dict() for i in Item.all()])


