# -*- coding: utf-8 -*-
from flask import Blueprint

api_gpu_model = Blueprint('gpuModel', __name__)


from . import gpuModel