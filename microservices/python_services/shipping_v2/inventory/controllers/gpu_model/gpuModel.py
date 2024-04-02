from flask import Blueprint, request, jsonify

from service.gpu_model.gpu_model_service import GpuModelService


from . import api_gpu_model

# GPU Model Routes
@api_gpu_model.route('/models', methods=['GET'])
def get_all_gpu_models():
    result, status = GpuModelService.get_all_gpu_models()
    return jsonify(result), status

@api_gpu_model.route('/model/list', methods=['GET'])
def list_gpu_models():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    query_params = {
        'ModelName': request.args.get('ModelName'),
        'Manufacturer': request.args.get('Manufacturer'),
    }
    query_params = {k: v for k, v in query_params.items() if v is not None}

    result = GpuModelService.list_gpu_models(page, per_page, query_params)
    return jsonify(result)

@api_gpu_model.route('/model', methods=['POST'])
def create_gpu_model():
    data = request.json
    result, status = GpuModelService.create_gpu_model(data)
    return jsonify(result), status

@api_gpu_model.route('/model/<int:model_id>', methods=['PUT'])
def update_gpu_model(model_id):
    data = request.json
    result, status = GpuModelService.update_gpu_model(model_id, data)
    return jsonify(result), status

@api_gpu_model.route('/model/<int:model_id>', methods=['DELETE'])
def delete_gpu_model(model_id):
    result, status = GpuModelService.delete_gpu_model(model_id)
    return jsonify(result), status

@api_gpu_model.route('/model/<int:model_id>', methods=['GET'])
def get_model(model_id):
    result, status = GpuModelService.get_model(model_id)
    return jsonify(result), status