import os

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flaskr.db import get_db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    cors = CORS(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/login', methods = ['POST'])
    @cross_origin()
    def login():
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if username is not None and password is not None:
            db = get_db()
            error = None
            try:
                check = db.execute(
                    "SELECT * FROM users WHERE email =? AND password =?",
                    (username, password),
                ).fetchone()
                if check is None:
                    error = "Incorrect email or password"
            except db.IntegrityError:
                error = "Database error"

            if error is None:
                return {"response": "ok"}
            else:
                return {"response": "error", "error": error}

    
    from . import db
    db.init_app(app)

    return app