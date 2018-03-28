import os
import sys
import logging

import unittest
from flask import Flask
from flask_pymongo import PyMongo
from config import *

from wallstreet.exceptions.configurations_exceptions import ImproperlyConfigured


ENVS = ['config.DevelopmentConfig', 'config.TestingConfig', 'config.StagingConfig', 'config.ProductionConfig']


def get_env_variable(var_name):
    """Get the environment variable or return exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f"Set the {var_name} environment variable"
        raise ImproperlyConfigured(error_msg)


try:
    env_aux = get_env_variable("ENV").lower()
    ENV = env_aux if env_aux in ENVS else 'config.DevelopmentConfig'
except ImproperlyConfigured:
    ENV = 'config.DevelopmentConfig'

app = Flask(__name__)
app.config['ENV'] = ENV
app.config.from_object(ENV)
app.mongo = PyMongo(app)

# app config
if ENV == ENVS[0]:
    # local development
    print("*** you should not see this message in production ***")

# log handler
log_level = logging.INFO if not app.config.get('DEBUG') else logging.DEBUG
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(log_level)
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))

for h in app.logger.handlers:
    app.logger.removeHandler(h)
app.logger.addHandler(handler)
app.logger.setLevel(log_level)

# import blueprints
from wallstreet.views import wallstreet

# register blueprints
app.register_blueprint(wallstreet, url_prefix='/currency')


@app.cli.command()
def test():
    """ Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('wallstreet/tests', pattern='*_tests.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    app.run(debug=True, port=9090)
