# -*- coding: utf-8 -*-
from flask import Blueprint

api_email = Blueprint('email', __name__)


from . import email
