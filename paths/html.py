import json

from lib.database_setup import User, Category, Item
from lib.session import (state_generator,
                         ensure_logged_in,
                         connect_user_through_google,
                         connect_user_through_facebook,
                         disconnect_user_through_google,
                         disconnect_user_through_facebook)



from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


def home():
    #return json.dumps([i.to_dict() for i in Item.all()])
    sess = dict(login_session)
    return render_template("homepage.html")

# Create anti-forgery state token
def login():
    state = state_generator()
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@ensure_logged_in
def logout(user):
    if login_session["provider"] == "google":
        disconnect_user_through_google()
    else:
        disconnect_user_through_facebook()
    login_session.clear()
    return redirect("/")


def fbconnect():
    import pdb;pdb.set_trace()
    connect_user_through_facebook(request)
    return "Logged in!"


def gconnect():
    connect_user_through_google(request)
    return "Logged in!"
