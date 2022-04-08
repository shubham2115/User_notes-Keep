from flask import Flask
from flask_mongoengine import MongoEngine
from flask_restful import Api
from routes import all_routes
from flask_caching import Cache
from dotenv import load_dotenv
from flask_restful_swagger import swagger



load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'
# api = Api(app)
api = swagger.docs(Api(app), apiVersion='0.1', api_spec_url='/docs')


# connecting with database
app.config['MONGODB_SETTINGS'] = {
    'db': 'Users_Notes',
}

db = MongoEngine(app)
config = {
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app.config.from_mapping(config)
cache = Cache(app)


# -------------------EndPoints---------------------------------


def confirm_api():
    for data in all_routes:
        api_class = data[0]
        endpoint = data[1]
        api.add_resource(api_class, endpoint)



confirm_api()

if __name__ == "__main__":
    app.run(debug=True, port=130)
