import os

from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin
from flaskr.db import get_db
from flaskr.users_model import Users
from flaskr.files_model import Files
from pathlib import Path

def format_response(data, error_message=""):
    if error_message == "":
        status = "ok"
    else:
        status = "error" 

    return { 
        "status": status, 
        "message": error_message,
        "data": data
    }

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

    def validateAuth(request, usersObj):
        headers = request.headers
        authToken = headers.get("Authorization")
        return usersObj.validateToken(authToken)

    #TODO: trebuie intors un token de autentificare care sa fie folosit la toate
    # celelalte endointuri
    # login
    @app.route('/api/v1/login', methods = ['POST'])
    @cross_origin()
    def login():
        usersClass = Users()
        data = request.json
        if data["email"] is not None and data["password"] is not None:
            user_data = [
                data["email"],
                data["password"]
            ]
            user = usersClass.getUserByEmailPassword(user_data)
            if user:
                user = user[0]
                del user['password']
                token = usersClass.getToken(user['user_id'])
                user['token'] = token
                response = format_response(user)
            else:
                response = format_response([], "Email or password invalid!")
            return response, 200

    # USERS
    @app.route('/api/v1/users', methods = ['POST', 'GET'])
    @cross_origin()
    def users():
        usersClass = Users()

        if request.method == 'POST':
            data = request.json
            user = usersClass.getUserByEmail([data["email"]])
            print (user)
            if not user:
                user_data = [
                    data["email"],
                    data["first_name"],
                    data["last_name"],
                    data["password"]
                ]
                users_list = usersClass.addUser(user_data)
                response = format_response(users_list)
                return response, 201
            else:
                response = format_response([],"Email already exists! Please login.")
                return response, 200
        
        if request.method == "GET":
            if (not validateAuth(request, usersClass)):
                response = format_response([],"Not Authorized!")
                return response, 401

            users_list = usersClass.getUsers()
            response = format_response(users_list)
            return response, 200

    #TODO:
    #POST upload a file
    #GET all files, o lista de fisiere
    @app.route('/api/v1/files', methods = ['POST', 'GET'])
    def upload():
        usersClass = Users()
        filesClass = Files()
        userList = validateAuth(request, usersClass)
        
        if (not userList):
                response = format_response([],"Not Authorized!")
                return response, 401
        
        user_id = userList[0][0]

        if request.method == 'POST':
            f = request.files['file']
            file_id = filesClass.addFile([user_id, f.filename])
            file_extension = f.filename.rsplit('.', 1)[1].lower()
            Path(f"documents/{user_id}").mkdir(parents=True, exist_ok=True)
            f.save(f"documents/{user_id}/{file_id}.{file_extension}")
            return_data = {
                "file_id": file_id,
                "user_id": user_id,
                "file_name": f.filename
            }
            return format_response(return_data)
            
        if request.method == 'GET':
            return format_response(filesClass.getFiles(user_id)), 200

    #TODO:
    #GET un fisier anume pentru visualizare
    @app.route('/api/v1/files/<file_id>', methods = ['GET'])
    def getFile(file_id):
        usersClass = Users()
        filesClass = Files()
        userList = validateAuth(request, usersClass)
        
        if (not userList):
                response = format_response([],"Not Authorized!")
                return response, 401
        
        if request.method == 'GET':
            file_details = filesClass.getFileDetails(file_id)
            if (not file_details):
                response = format_response([], "Not Found!")
                return response, 404
            
            file_details = file_details[0]
            file_id = file_details["file_id"]
            file_user_id = file_details["user_id"]
            file_extension = file_details['file_name'].rsplit('.', 1)[1].lower()

            return send_file(f"../documents/{file_user_id}/{file_id}.{file_extension}", as_attachment=False)

    #TODO:
    #GET detalii fiser: daca e ok, un status: citit, necitit, aprobat, neaprobat
    #POST si sau UPDATE detalii fisier: se modifica statusurile fisierului
    #@app.route('/api/v1/files/<id>/details', methods = ['GET', 'POST'])

    from . import db
    db.init_app(app)

    return app