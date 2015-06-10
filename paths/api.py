from dict2xml import dict2xml
from flask import render_template, request, jsonify

from lib.database_setup import Category, Item


def generate_catalog():
    response = []
    for category in Category.all():
        response.append({
            "name": category.name,
            "user_id": category.user_id,
            "picture": category.picture,
            "items": [item.to_dict() for item in Item.find(category_id=category.id)]
        })
    return {"categories": response}


def catalog_json():
    categories = generate_catalog()
    return jsonify(**categories)

def catalog_xml():
    categories = generate_catalog()
    return dict2xml(categories)

def categories_json():
    categories = [categ.to_dict() for categ in Category.all()]
    return jsonify(categories=categories)

def categories_xml():
    categories = [categ.to_dict() for categ in Category.all()]
    return dict2xml({"categories": categories})

def items_json():
    items = [item.to_dict() for item in Item.all()]
    return jsonify(items=items)

def items_xml():
    items = [item.to_dict() for item in Item.all()]
    return dict2xml({"items": items})
