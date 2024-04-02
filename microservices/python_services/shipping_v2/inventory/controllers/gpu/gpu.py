from flask import Blueprint, request, jsonify

from service.gpu.gpu_service import GpuService


from . import api_gpu


# GPU Routes
@api_gpu.route('/gpus', methods=['GET'])
def get_all_gpus():
    result, status = GpuService.get_all_gpus()
    return jsonify(result), status

@api_gpu.route('/gpu/list', methods=['GET'])
def list_gpus():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    query_params = {
        'SerialNumber': request.args.get('SerialNumber'),
        'ModelID': request.args.get('ModelID'),
    }
    query_params = {k: v for k, v in query_params.items() if v is not None}

    result = GpuService.list_gpus(page, per_page, query_params)
    return jsonify(result)

@api_gpu.route('/gpu', methods=['POST'])
def create_gpu():
    data = request.json
    result, status = GpuService.create_gpu(data)
    return jsonify(result), status

@api_gpu.route('/gpu/<int:serial_number>', methods=['PUT'])
def update_gpu(serial_number):
    data = request.json
    result, status = GpuService.update_gpu(serial_number, data)
    return jsonify(result), status

@api_gpu.route('/gpu/<int:serial_number>', methods=['DELETE'])
def delete_gpu(serial_number):
    result, status = GpuService.delete_gpu(serial_number)
    return jsonify(result), status
