import logging
from flask import Flask

# Create Flask application
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nioqedkc:L_hHgWLL5NXt1I7PzgG4Dddro37nXNAt@baasu.db.elephantsql.com:5432/nioqedkc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Shhhh'
app.config['LOGGING_LEVEL'] = logging.INFO

import os
import service, model
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')

# Set up logging for production
print('Setting up logging for {}...'.format(__name__))
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    if gunicorn_logger:
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

app.logger.info('Logging established')
app.logger.info("**********************************************")
app.logger.info(" P R O D U C T   S E R V I C E   R U N N I N G")
app.logger.info("**********************************************")
service.init_db()
# app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)