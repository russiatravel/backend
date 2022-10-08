import logging

from backend.places.views import app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    logger.info('Started successfully')
    app.run()


if __name__ == '__main__':
    main()
