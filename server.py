import os
import sys
from flask import Flask, redirect
from flask import session as login_session

from paths import ROUTES
from lib.session import state_generator
from lib.exceptions import APPException



#Add current path to sys paths
PATH = os.path.realpath('.')
sys.path.append(PATH)


#Start app engine
app = Flask(__name__)
app.secret_key = "Super secret KEY"


#Add rules to the app
for methods, path, func in ROUTES:
    app.add_url_rule(path, view_func=func, methods=methods)


#Add exception handler
@app.errorhandler(APPException)
def exception_handler(error):
    BASE_URL = "/error?code={}&message={}"
    url = BASE_URL.format(error.status_code, error.message)
    return redirect(url)


#Send session with every request
@app.context_processor
def inject_user():
    state = login_session.get("state")
    if not login_session.get("state") :
        login_session["state"] = state_generator()
    return dict(sess=dict(login_session))



#Start server
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
