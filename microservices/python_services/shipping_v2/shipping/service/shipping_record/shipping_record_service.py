from datetime import datetime
from extensions import db 
from models import ShippingRecord  
from flask import request, jsonify, current_app

from service.mq_product.mq_producer_service import MQProducerService

class ShippingRecordService:

    @staticmethod
    def get_all_shipping_records():
        try:
            records = ShippingRecord.query.all()
            records_list = []
            for record in records:
                record_dict = {column.name: getattr(record, column.name) for column in record.__table__.columns}
                records_list.append(record_dict)
            return {'status': 'success', 'data': records_list}, 200
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500
        
    def list_shipping_records(page=1, per_page=10, query_params=None, order_by='ReceivedDateTime', order_direction='desc'):
        try:
            if query_params is None:
                query_params = {}

            shipping_in_id = query_params.get('ShippingInID', None)
            shipping_out_id = query_params.get('ShippingOutID', None)
            received_date_start = query_params.get('ReceivedDateStart', None)
            received_date_end = query_params.get('ReceivedDateEnd', None)
            remark = query_params.get('Remarks', None)

            query = ShippingRecord.query

            if shipping_in_id:
                query = query.filter(ShippingRecord.ShippingInID == shipping_in_id)
            if shipping_out_id:
                query = query.filter(ShippingRecord.ShippingOutID == shipping_out_id)
            if received_date_start:
                query = query.filter(ShippingRecord.ReceivedDateTime >= received_date_start)
            if received_date_end:
                query = query.filter(ShippingRecord.ReceivedDateTime <= received_date_end)
            if remark:
                query = query.filter(ShippingRecord.Remarks.like(f"%{remark}%"))

            if order_direction == 'desc':
                query = query.order_by(getattr(ShippingRecord, order_by).desc())
            else:
                query = query.order_by(getattr(ShippingRecord, order_by).asc())

            paginated_records = query.paginate(page=page, per_page=per_page, error_out=False)
            items = paginated_records.items

            return {
                'items': [item.to_dict() for item in items],
                'total': paginated_records.total,
                'pages': paginated_records.pages,
                'page': page
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500





    @staticmethod
    def create_shipping_record(data):
        try:
            record = ShippingRecord.query.filter_by(CaseID=data['CaseID']).first()    
            if record:
                for key, value in data.items():
                    if hasattr(record, key):  
                        if(key == 'Remarks'):
                            order_code = data.get('Remarks', '')
                            value = ShippingRecordService.update_remarks(record, order_code)
                        setattr(record, key, value)
                    else:
                        print(f"Warning: Trying to update non-existent field {key} for ShippingRecord.")
                db.session.commit()
                return {'status': 'success', 'message': 'Record successfully updated.'}, 200
            else:
                data['ReceivedDateTime'] = datetime.utcnow()
                record = ShippingRecord(**data)
                db.session.add(record)
            
            db.session.commit()
            return {'data': data, 'message': 'Record updated' if record else 'Record created'}, 200

        except Exception as e:
            db.session.rollback()
            return {'status': 'error', 'message': str(e)}, 500

    @staticmethod
    def update_shipping_record(case_id, data, order_code):
        try:
            record = ShippingRecord.query.filter_by(CaseID=case_id).first()
            
            if not record:
                return {'status': 'error', 'message': 'Record not found.'}, 404

            for key, value in data.items():
                if hasattr(record, key):  
                    if(key == 'Remarks'):
                            order_code = data.get('Remarks', '')
                            value = ShippingRecordService.update_remarks(record, order_code)
                    setattr(record, key, value)
                else:
                    print(f"Warning: Trying to update non-existent field {key} for ShippingRecord.")
            db.session.commit()
            return {'status': 'success', 'message': 'Record successfully updated.'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'status': 'error', 'message': str(e)}, 500
    
    @staticmethod
    def update_remarks(record, order_code):
        if order_code == '0':
            return 'returned original'
        elif order_code == '1':
            return 'replaced same'
        elif order_code == '2':
            return 'replace alternative'
        else:
            return ''

    @staticmethod
    def delete_shipping_record(case_id):
        try:
            record = ShippingRecord.query.filter_by(CaseID=case_id).first()
            if record:
                db.session.delete(record)
                db.session.commit()
                return {'status': 'success', 'message': 'Record successfully deleted.'}, 200
            return {'status': 'error', 'message': 'Record not found.'}, 404
        except Exception as e:
            db.session.rollback()
            return {'status': 'error', 'message': str(e)}, 500

    @staticmethod
    def get_shipping_record(case_id):
        try:
            record = ShippingRecord.query.filter_by(CaseID=case_id).first()
            if record:
                # Assuming you have a method to serialize your SQLAlchemy model to a dict
                record_dict = {column.name: getattr(record, column.name) for column in record.__table__.columns}
                return {'status': 'success', 'data': record_dict}, 200
            return {'status': 'error', 'message': 'Record not found.'}, 404
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500
