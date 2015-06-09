import os
import sys
from flask import Flask
from paths import ROUTES

#Add current path to sys paths
PATH = os.path.realpath('.')
sys.path.append(PATH)


#Start app engine
app = Flask(__name__)
app.secret_key = "Super secret KEY"

#Add rules to the app
for methods, path, func in ROUTES:
    app.add_url_rule(path, view_func=func, methods=methods)


#Start server
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
