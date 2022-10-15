import logging

from flask import Flask
from pydantic import ValidationError
from backend.database import db_session
from backend.errors import AppError
from backend.places.views import place_view
from backend.cities.views import city_view

app = Flask(__name__)
app.register_blueprint(place_view, url_prefix='/api/places')
app.register_blueprint(city_view, url_prefix='/api/cities')


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def shutdown_session(exception=None):
    db_session.remove()


def handle_app_error(err: AppError):
    return {'error': str(err)}, err.code


def handle_validation_error(err: ValidationError):
    return {'error': str(err)}, 400


app.register_error_handler(AppError, handle_app_error)
app.register_error_handler(ValidationError, handle_validation_error)
app.teardown_appcontext(shutdown_session)


def main():
    logger.info('Started successfully')
    app.run()


if __name__ == '__main__':
    main()
