import json
from flask import session as login_session
from flask import render_template, request, redirect, url_for

from lib.database_setup import User, Category, Item
from lib import session


def home():
    left_content = [item.to_dict() for item in Category.all()]
    right_content = [item.to_full_dict() for item in Item.all(10)]
    data = {
        "right_title": "Last items",
        "left_content": left_content,
        "right_content": right_content,
        "with_parrent": True
    }
    return render_template("listing.html", data=data)

def error():
    message = request.values.get("message", "An error has occured")
    code = request.values.get("code", 500)
    return render_template("error.html", message=message, code=code)

def category(category_id):
    category = Category(id=category_id).get()
    left_content = [item.to_dict() for item in Category.all()]
    right_content = [item.to_dict() for item in Item.find(category_id=category_id)]
    data = {
        "category": category.to_dict(),
        "right_title": "{} Items ({} items)".format(category.name, len(right_content)),
        "left_content": left_content,
        "right_content": right_content,
        "with_parrent": False
    }
    return render_template("listing.html", data=data)


def item(item_id):
    item = Item(id=item_id).get()
    return render_template("item.html", data=item.to_dict())


@session.ensure_logged_in
def create_item(user):
    if request.method == 'POST':
        category_id = int(request.form["category_id"])
        item = Item(name=request.form["name"],
                    description=request.form["description"],
                    user_id=login_session["user_id"],
                    category_id=category_id,
                    category=Category(id=category_id).get()
                    ).create()
        item.add_picture(request)
        return redirect(url_for("item", item_id=item.id))
    else:
        data = {
            "type": "item",
            "action": "Create",
            "categories": [item.to_dict() for item in Category.all()]
        }
        return render_template("create_edit.html", data=data)


@session.ensure_logged_in
def edit_item(user, item_id):
    item = Item(id=item_id).get()
    session.ensure_permission(user, item)
    if request.method == 'POST':
        category_id = int(request.form["category_id"])
        item.name=request.form["name"]
        item.description=request.form["description"]
        item.category_id=category_id
        item.category=Category(id=category_id).get()
        item.save()
        item.add_picture(request)
        return redirect(url_for("item", item_id=item_id))
    else:
        data=item.to_dict()
        data["type"] = "item"
        data["action"] = "Edit"
        data["categories"] = [item.to_dict() for item in Category.all()]
        return render_template("create_edit.html", data=data)


@session.ensure_logged_in
def delete_item(user, item_id):
    item = Item(id=item_id).get()
    session.ensure_permission(user, item)
    if request.method == 'POST':
        item.delete()
        return redirect(url_for("home"))
    else:
        data=item.to_dict()
        data["type"] = "item"
        return render_template("delete.html", data=data)



@session.ensure_logged_in
def create_category(user):
    if request.method == 'POST':
        category = Category(name=request.form["name"],
                            user_id=login_session["user_id"]
                            ).create()
        category.add_picture(request)
        return redirect(url_for("category", category_id=category.id))
    else:
        data = {
            "type": "category",
            "action": "Create"
        }
        return render_template("create_edit.html", data=data)


@session.ensure_logged_in
def edit_category(user, category_id):
    category = Category(id=category_id).get()
    session.ensure_permission(user, category)
    if request.method == 'POST':
        category.name=request.form["name"]
        category.save()
        category.add_picture(request)
        return redirect(url_for("category", category_id=category_id))
    else:
        data=category.to_dict()
        data["type"] = "category"
        data["action"] = "Edit"
        return render_template("create_edit.html", data=data)


@session.ensure_logged_in
def delete_category(user, category_id):
    category = Category(id=category_id).get()
    session.ensure_permission(user, category)
    if request.method == 'POST':
        items = [item.delete() for item in Item.find(category_id=category_id)]
        category.delete()
        return redirect(url_for("home"))
    else:
        data=category.to_dict()
        data["type"] = "category and all sub-items"
        return render_template("delete.html", data=data)


def fbconnect():
    session.connect_user_through_facebook(request)
    return "Logged in!"

def gconnect():
    session.connect_user_through_google(request)
    return "Logged in!"

@session.ensure_logged_in
def logout(user):
    if login_session["provider"] == "google":
        session.disconnect_user_through_google()
    else:
        session.disconnect_user_through_facebook()
    login_session.clear()
    return redirect("/")


