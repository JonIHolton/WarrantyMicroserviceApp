# -*- coding: utf-8 -*-
from flask import Blueprint

api_gpu = Blueprint('gpu', __name__)


from . import gpu
