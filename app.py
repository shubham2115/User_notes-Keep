from flask import Flask, jsonify, request, make_response
from flask_mongoengine import MongoEngine
from flask_restful import Api, Resource

from notes import AddNote
from routes import all_routes
from user.apis import Registration, Activate, Login, LogOut
from notes.apis import Home

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'
api = Api(app)

# connecting with database
app.config['MONGODB_SETTINGS'] = {
    'db': 'Users_Notes',
}

db = MongoEngine(app)


# -------------------EndPoints---------------------------------
# def confirm_api():
#     for data in all_routes:
#         api_class = data[0]
#         endpoint = data[1]
#         api.add_resource(api_class, endpoint)
api.add_resource(Registration,'/')
api.add_resource(Login,'/login')
api.add_resource(AddNote,'/note')
api.add_resource(LogOut,'/logout')
api.add_resource(Home,'/')

if __name__ == "__main__":
    app.run(debug=True, port=130)
