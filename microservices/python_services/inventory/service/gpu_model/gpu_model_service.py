from extensions import db
from models import Gpu, GpuModel

class GpuModelService:

    @staticmethod
    def get_all_gpu_models():
        try:
            models = GpuModel.query.all()
            models_list = []
            for model in models:
                model_dict = {column.name: getattr(model, column.name) for column in model.__table__.columns}
                models_list.append(model_dict)
            return {'status': 'success', 'data': models_list}, 200
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500
        
    @staticmethod
    def list_gpu_models(page=1, per_page=10, query_params=None):
        try:
            if query_params is None:
                query_params = {}

            model_name = query_params.get('ModelName', None)
            manufacturer = query_params.get('Manufacturer', None)

            query = GpuModel.query

            if model_name:
                query = query.filter(GpuModel.ModelName.like(f"%{model_name}%"))
            if manufacturer:
                query = query.filter(GpuModel.Manufacturer.like(f"%{manufacturer}%"))

            paginated_models = query.paginate(page=page, per_page=per_page, error_out=False)
            models = paginated_models.items

            return {
                'items': [model.to_dict() for model in models],
                'total': paginated_models.total,
                'pages': paginated_models.pages,
                'page': page
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500

    @staticmethod
    def create_gpu_model(data):
        try:
            new_model = GpuModel(**data)
            db.session.add(new_model)
            db.session.commit()
            return {'status': 'success', 'message': 'GPU model successfully created.'}, 200
        except Exception as e:
            db.session.rollback()
            return {'status': 'error', 'message': str(e)}, 500

    @staticmethod
    def update_gpu_model(model_id, data):
        try:
            model = GpuModel.query.filter_by(ModelID=model_id).first()
            if model:
                for key, value in data.items():
                    setattr(model, key, value)
                db.session.commit()
                return {'status': 'success', 'message': 'GPU model successfully updated.'}, 200
            return {'status': 'error', 'message': 'GPU model not found.'}, 404
        except Exception as e:
            db.session.rollback()
            return {'status': 'error', 'message': str(e)}, 500

    @staticmethod
    def delete_gpu_model(model_id):
        try:
            model = GpuModel.query.filter_by(ModelID=model_id).first()
            if model:
                db.session.delete(model)
                db.session.commit()
                return {'status': 'success', 'message': 'GPU model successfully deleted.'}, 200
            return {'status': 'error', 'message': 'GPU model not found.'}, 404
        except Exception as e:
            db.session.rollback()
            return {'status': 'error', 'message': str(e)}, 500
        

    @staticmethod
    def get_model(model_id):
        try:
            record = GpuModel.query.filter_by(ModelID=model_id).first()
            if record:
                record_dict = {column.name: getattr(record, column.name) for column in record.__table__.columns}
                return {'status': 'success', 'data': record_dict}, 200
            return {'status': 'error', 'message': 'Record not found.'}, 404
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500
