from flask import Blueprint, request, jsonify
from datetime import datetime
from service.inventory.inventory_service import InventoryService

from . import api_inventory


@api_inventory.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'success'}), 200

@api_inventory.route('/inventory/all', methods=['GET'])
def get_all_inventory_items():
    result, status = InventoryService.get_all_inventory_items()
    return jsonify(result), status

@api_inventory.route('/inventory/list', methods=['GET'])
def list_inventory_items():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    order_by = request.args.get('order_by', 'Model')
    order_direction = request.args.get('order_direction', 'desc')

    query_params = {
        'SerialNumber': request.args.get('SerialNumber'),
        'Model': request.args.get('Model'),
        'Condition': request.args.get('Condition'),
        'Status': request.args.get('Status'),  
        'ReturnAddress': request.args.get('ReturnAddress'),  
    }



    query_params = {k: v for k, v in query_params.items() if v is not None}

    result = InventoryService.list_inventory_items(page, per_page, query_params, order_by, order_direction)
    return jsonify(result)

@api_inventory.route('/inventory', methods=['POST'])
def create_inventory_item():
    data = request.json
    result, status = InventoryService.create_inventory_item(data)
    return jsonify(result), status

@api_inventory.route('/inventory/<int:inventory_id>', methods=['GET'])
def get_inventory_item(inventory_id):
    result, status = InventoryService.get_inventory_item(inventory_id)
    return jsonify(result), status

@api_inventory.route('/inventory/<int:inventory_id>', methods=['PUT'])
def update_inventory_item(inventory_id):
    data = request.json
    result, status = InventoryService.update_inventory_item(inventory_id, data)
    return jsonify(result), status

@api_inventory.route('/inventory/<int:inventory_id>', methods=['DELETE'])
def delete_inventory_item(inventory_id):
    result, status = InventoryService.delete_inventory_item(inventory_id)
    return jsonify(result), status
