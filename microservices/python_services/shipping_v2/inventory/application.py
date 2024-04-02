# -*- coding: utf-8 -*-

from flask import Flask
from settings import DevelopmentConfig
from controllers.mq import api_mq
from controllers.gpu import api_gpu
from controllers.gpu_model import api_gpu_model;
from controllers.inventory import api_inventory
from extensions import db


PROJECT_NAME = 'Warranty_Claims_Inventory'


def create_app(config=None):
    app = Flask(PROJECT_NAME)
    configure_app(app, config)
    configure_extensions(app)
    configure_blueprints(app)
    configure_logging(app)

    app.debug_logger.debug('------ '+ PROJECT_NAME + ' ------')

    return app


def configure_app(app, config):
    if not config:
        config = DevelopmentConfig

    app.config.from_object(config)


def configure_extensions(app):

    db.init_app(app)


def configure_logging(app):

    import logging
    from logging import StreamHandler

    class DebugHandler(StreamHandler):
        def emit(x, record):
            StreamHandler.emit(x, record) if app.debug else None

    logger = logging.getLogger('app')
    logger.addHandler(DebugHandler())
    logger.setLevel(logging.DEBUG)

    app.debug_logger = logger


def configure_blueprints(app):
    app.register_blueprint(api_mq, url_prefix='/api/mq')
    app.register_blueprint(api_gpu, url_prefix='/api/inventory')
    app.register_blueprint(api_gpu_model, url_prefix='/api/inventory')
    app.register_blueprint(api_inventory, url_prefix='/api/inventory')

