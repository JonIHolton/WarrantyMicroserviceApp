from extensions import db
from models import Gpu, GpuModel

class GpuService:

    @staticmethod
    def get_all_gpus():
        try:
            gpus = Gpu.query.all()
            gpus_list = []
            for gpu in gpus:
                gpu_dict = {column.name: getattr(gpu, column.name) for column in gpu.__table__.columns}
                gpus_list.append(gpu_dict)
            return {'status': 'success', 'data': gpus_list}, 200
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500
        
    @staticmethod
    def list_gpus(page=1, per_page=10, query_params=None):
        try:
            if query_params is None:
                query_params = {}

            serial_number = query_params.get('SerialNumber', None)
            model_id = query_params.get('ModelID', None)

            query = Gpu.query

            if serial_number:
                query = query.filter(Gpu.SerialNumber == serial_number)
            if model_id:
                query = query.filter(Gpu.ModelID == model_id)

            paginated_gpus = query.paginate(page=page, per_page=per_page, error_out=False)
            gpus = paginated_gpus.items

            return {
                'items': [gpu.to_dict() for gpu in gpus],
                'total': paginated_gpus.total,
                'pages': paginated_gpus.pages,
                'page': page
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500

    @staticmethod
    def create_gpu(data):
        try:
            new_gpu = Gpu(**data)
            db.session.add(new_gpu)
            db.session.commit()
            return {'status': 'success', 'message': 'GPU successfully created.'}, 200
        except Exception as e:
            db.session.rollback()
            return {'status': 'error', 'message': str(e)}, 500

    @staticmethod
    def update_gpu(serial_number, data):
        try:
            gpu = Gpu.query.filter_by(SerialNumber=serial_number).first()
            if gpu:
                for key, value in data.items():
                    setattr(gpu, key, value)
                db.session.commit()
                return {'status': 'success', 'message': 'GPU successfully updated.'}, 200
            return {'status': 'error', 'message': 'GPU not found.'}, 404
        except Exception as e:
            db.session.rollback()
            return {'status': 'error', 'message': str(e)}, 500

    @staticmethod
    def delete_gpu(serial_number):
        try:
            gpu = Gpu.query.filter_by(SerialNumber=serial_number).first()
            if gpu:
                db.session.delete(gpu)
                db.session.commit()
                return {'status': 'success', 'message': 'GPU successfully deleted.'}, 200
            return {'status': 'error', 'message': 'GPU not found.'}, 404
        except Exception as e:
            db.session.rollback()
            return {'status': 'error', 'message': str(e)}, 500
