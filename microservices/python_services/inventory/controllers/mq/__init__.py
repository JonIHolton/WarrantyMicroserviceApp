# -*- coding: utf-8 -*-
from flask import Blueprint

api_mq = Blueprint('mq', __name__)


from . import mq
