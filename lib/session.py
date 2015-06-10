import httplib2
import json
import random
import string
import requests
import functools
from flask import make_response
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

from lib import exceptions
from lib.database_setup import User


FACEBOOK_ID = "860829713952701"
FACEBOOK_SECRET = "0f30a94e8f8a857dd1d92a408dc96f7a"
GOOGLE_ID = "271058424614-k1icmfnvp1msujq6tbn6oehmjrtnksgn.apps.googleusercontent.com"


def ensure_logged_in(func):

    @functools.wraps(func)
    def inner(*args, **kwargs):
        user_id = login_session.get("user_id")
        if not user_id:
            raise exceptions.AuthenticationRequired()
        user = User(id=user_id).get()
        return func(user, *args, **kwargs)
    return inner


def ensure_permission(user, entity):
    if user.id != entity.user_id:
        raise exceptions.Unauthorized()


def state_generator():
    uid = "".join(random.choice(string.ascii_uppercase + string.digits)
                  for i in xrange(32))
    return uid


def connect_user_through_google(request):
    # Validate state token
    if request.args.get("state") != login_session["state"]:
        response = make_response(json.dumps("Invalid state parameter."), 401)
        response.headers["Content-Type"] = "application/json"
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets("config/google.json", scope="")
        oauth_flow.redirect_uri = "postmessage"
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps("Failed to upgrade the authorization code."), 401)
        response.headers["Content-Type"] = "application/json"
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ("https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s"
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, "GET")[1])
    # If there was an error in the access token info, abort.
    if result.get("error") is not None:
        response = make_response(json.dumps(result.get("error")), 500)
        response.headers["Content-Type"] = "application/json"

    # Verify that the access token is used for the intended user.
    provider_id = credentials.id_token["sub"]
    if result["user_id"] != provider_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers["Content-Type"] = "application/json"
        return response

    # Verify that the access token is valid for this app.
    if result["issued_to"] != "271058424614-k1icmfnvp1msujq6tbn6oehmjrtnksgn.apps.googleusercontent.com":
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers["Content-Type"] = "application/json"
        return response

    if login_session.get("access_token") is not None and \
            provider_id == login_session.get("provider_id"):
        response = make_response(json.dumps("Current user is already connected."), 200)
        response.headers["Content-Type"] = "application/json"
        return response

    # Store the access token in the session for later use.

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {"access_token": credentials.access_token, "alt": "json"}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()


    # see if user exists, if it doesn"t make a new one
    user = User.findone(email=data["email"])
    if not user:
        user = User(name=data["name"],
                    email=data["email"],
                    picture=data["picture"]).create()
    login_session["user_id"] = user.id
    login_session["user"] = user.to_dict()
    login_session["provider"] = "google"
    login_session["provider_id"] = provider_id
    login_session["access_token"] = credentials.access_token



def connect_user_through_facebook(request):

    if request.args.get("state") != login_session["state"]:
        response = make_response(json.dumps("Invalid state parameter."), 401)
        response.headers["Content-Type"] = "application/json"
        return response
    access_token = request.data

    app_id = FACEBOOK_ID
    app_secret = FACEBOOK_SECRET
    url = "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s" % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, "GET")[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.2/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    # Get user picture
    url = "https://graph.facebook.com/v2.2/me/picture?%s&redirect=0&height=200&width=200" % token
    h = httplib2.Http()
    result = h.request(url, "GET")[1]
    data = json.loads(result)
    picture = data["data"]["url"]

    #Get user data
    url = "https://graph.facebook.com/v2.2/me?%s" % token
    h = httplib2.Http()
    result = h.request(url, "GET")[1]
    data = json.loads(result)

    # The token must be stored in the login_session in order to properly logout, let"s strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]

    # see if user exists
    user = User.findone(email=data["email"])
    if not user:
        user = User(name=data["name"],
                    email=data["email"],
                    picture=picture).create()
    login_session["user"] = user.to_dict()
    login_session["user_id"] = user.id
    login_session["provider"] = "facebook"
    login_session["provider_id"] = data["id"]
    login_session["access_token"] = stored_token



def disconnect_user_through_facebook():
    provider_id = login_session["provider_id"]
    access_token = login_session["access_token"]
    url = "https://graph.facebook.com/%s/permissions" % (provider_id)
    h = httplib2.Http()
    result = h.request(url, "DELETE")[1]


def disconnect_user_through_google():
    access_token = login_session.get("access_token")
    url = "https://accounts.google.com/o/oauth2/revoke?token=%s" % access_token
    h = httplib2.Http()
    result = h.request(url, "GET")[0]
