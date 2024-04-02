# -*- coding: utf-8 -*-

import os

class Config(object):
    DEBUG = False
    # mail settings
    MAIL_SERVER = 'smtp.126.com'
    MAIL_PORT = 25
    # mail authentication
    MAIL_USERNAME = 'bababa'
    MAIL_PASSWORD = 'bababa'
    # RabbitMQ Default Configuration
    RABBITMQ_HOST = 'rabbitmq-service'
    RABBITMQ_QUEUE = 'Email'
    RABBITMQ_WORKING_FLAG = 'Y'

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    # database
    SQLALCHEMY_DATABASE_URI = 'mysql://root:rootpassword@inventory-shipping-db:3306/inventory'
    SQLALCHEMY_ECHO = True
    # RabbitMQ Development Configuration
    RABBITMQ_HOST = 'rabbitmq-service'
    RABBITMQ_QUEUE = 'Email'
    RABBITMQ_WORKING_FLAG = 'Y'

class StagingConfig(Config):
    ENV = 'staging'
    DEBUG = True
    # database
    SQLALCHEMY_DATABASE_URI = 'mysql://root:rootpassword@inventory-shipping-db:3306/inventory'
    SQLALCHEMY_ECHO = True
    # RabbitMQ Staging Configuration
    RABBITMQ_HOST = 'rabbitmq-service'
    RABBITMQ_QUEUE = 'Email'
    RABBITMQ_WORKING_FLAG = 'Y'

class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    # database
    SQLALCHEMY_DATABASE_URI = 'mysql://root:rootpassword@inventory-shipping-db:3306/inventory'
    SQLALCHEMY_ECHO = True
    # RabbitMQ Production Configuration
    RABBITMQ_HOST = 'rabbitmq-service'
    RABBITMQ_QUEUE = 'Email'
    RABBITMQ_WORKING_FLAG = 'Y'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
