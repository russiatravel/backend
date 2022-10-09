import logging

from flask import Flask
from pydantic import ValidationError

from backend.errors import AppError
from backend.places.views import place_view

app = Flask(__name__)
app.register_blueprint(place_view, url_prefix='/api/places')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_app_error(err: AppError):
    return {'error': str(err)}, err.code


def handle_validation_error(err: ValidationError):
    return {'error': str(err)}, 400


app.register_error_handler(AppError, handle_app_error)
app.register_error_handler(ValidationError, handle_validation_error)


def main():
    logger.info('Started successfully')
    app.run()


if __name__ == '__main__':
    main()
