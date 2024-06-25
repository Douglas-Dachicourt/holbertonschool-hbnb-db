import os
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, current_app
#from flask_jwt_extended import JWTManager
from api.user_api import user_api
# from api.country_api import country_api
# from api.place_api import place_api
# from api.amenities_api import amenities_api
# from api.review_api import review_api
# from api.cities_api import cities_api

from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///development.db'
#app.config['JWT_SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
#jwt =JWTManager(app)

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
)

app.register_blueprint(swaggerui_blueprint)
app.register_blueprint(user_api)
# app.register_blueprint(country_api)
# app.register_blueprint(place_api)
# app.register_blueprint(amenities_api)
# app.register_blueprint(review_api)
# app.register_blueprint(cities_api)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    port = os.getenv("PORT",5000)

    app.run(debug=True, host='0.0.0.0', port=port)
