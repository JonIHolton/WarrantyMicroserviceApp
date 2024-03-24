import requests
from flask import  request ,jsonify

from datetime import datetime

from service.shipping_record.shipping_record_service import ShippingRecordService

from . import api_shipping_record

@api_shipping_record.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'success'}), 200

@api_shipping_record.route('/shippingrecords/all', methods=['GET'])
def get_all_records():
    result, status = ShippingRecordService.get_all_shipping_records()
    return jsonify(result), status

@api_shipping_record.route('/shippingrecords/list', methods=['GET'])
def get_shipping_records():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    order_by = request.args.get('order_by', 'ReceivedDateTime')
    order_direction = request.args.get('order_direction', 'desc')

    query_params = {
        'ShippingInID': request.args.get('ShippingInID'),
        'ShippingOutID': request.args.get('ShippingOutID'),
        'Remarks': request.args.get('Remarks'),
        'ReceivedDateStart': request.args.get('ReceivedDateStart'),
        'ReceivedDateEnd': request.args.get('ReceivedDateEnd')
    }

    query_params = {k: v for k, v in query_params.items() if v is not None}

    if 'ReceivedDateStart' in query_params:
        query_params['ReceivedDateStart'] = datetime.strptime(query_params['ReceivedDateStart'], '%Y-%m-%d')

    if 'ReceivedDateEnd' in query_params:
        query_params['ReceivedDateEnd'] = datetime.strptime(query_params['ReceivedDateEnd'], '%Y-%m-%d')

    result = ShippingRecordService.list_shipping_records(page, per_page, query_params,order_by,order_direction)
    return jsonify(result)

@api_shipping_record.route('/shippingrecords', methods=['POST'])
def create_shipping_record():
    data = request.json
    result, status = ShippingRecordService.create_shipping_record(data)
    return jsonify(result), status

@api_shipping_record.route('/shippingrecords/<case_id>', methods=['GET'])
def get_shipping_record(case_id):
    result, status = ShippingRecordService.get_shipping_record(case_id)
    return jsonify(result), status

@api_shipping_record.route('/shippingrecords/<case_id>', methods=['PUT'])
def update_shipping_record(case_id):
    data = request.json
    result, status = ShippingRecordService.update_shipping_record(case_id, data)
    return jsonify(result), status

@api_shipping_record.route('/shippingrecords/<case_id>', methods=['DELETE'])
def delete_shipping_record(case_id):
    result, status = ShippingRecordService.delete_shipping_record(case_id)
    return jsonify(result), status