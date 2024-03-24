# -*- coding: utf-8 -*-
from flask import Blueprint

api_inventory = Blueprint('inventory', __name__)


from . import inventory
