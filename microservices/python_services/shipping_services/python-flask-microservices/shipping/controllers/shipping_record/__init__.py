# -*- coding: utf-8 -*-
from flask import Blueprint

api_shipping_record = Blueprint('shipping_record', __name__)


from . import shipping_record
