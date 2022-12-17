from loguru import logger

from src.app import app


if __name__ == '__main__':
    logger.add('logs/logfile.log', format='{time} | {level} | {message}', level='DEBUG',
               rotation='05:00', retention='7 days', compression='zip')
    logger.info('Start')
    app.run( host='0.0.0.0')
