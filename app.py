from flask import Flask
from flask_mongoengine import MongoEngine
from flask_restful import Api
from routes import all_routes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'
api = Api(app)

# connecting with database
app.config['MONGODB_SETTINGS'] = {
    'db': 'Users_Notes',
}

db = MongoEngine(app)


# -------------------EndPoints---------------------------------
def confirm_api():
    for data in all_routes:
        api_class = data[0]
        endpoint = data[1]
        api.add_resource(api_class, endpoint)


confirm_api()

if __name__ == "__main__":
    app.run(debug=True, port=130)
