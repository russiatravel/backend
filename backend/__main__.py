from asyncio.log import logger
import logging
from backend.places import app


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    logger.info('Started successfully')
    app.run()


if __name__ == '__main__':
    main()
