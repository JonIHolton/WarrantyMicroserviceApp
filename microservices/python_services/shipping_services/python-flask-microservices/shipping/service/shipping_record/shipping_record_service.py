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
            record = ShippingRecord(**data)
            db.session.add(record)
            db.session.commit()
            # Send Request ID and Shipping via RabbitMQ
            message_content = '{"RequestID":1,"Shipping":{"key":"value"}}'
            host = current_app.config['RABBITMQ_HOST']
            queue_name = current_app.config['RABBITMQ_QUEUE']
            producer = MQProducerService(host, queue_name)
            try:
                producer.send_message(message_content)
                return jsonify({'status': 'success', 'message': 'Message sent successfully'}), 200
            finally:
                producer.close_connection()

        except Exception as e:
            db.session.rollback()
            return {'status': 'error', 'message': str(e)}, 500

    @staticmethod
    def update_shipping_record(case_id, data):
        try:
            record = ShippingRecord.query.filter_by(CaseID=case_id).first()
            if record:
                for key, value in data.items():
                    setattr(record, key, value)
                db.session.commit()
                return {'status': 'success', 'message': 'Record successfully updated.'}, 200
            return {'status': 'error', 'message': 'Record not found.'}, 404
        except Exception as e:
            db.session.rollback()
            return {'status': 'error', 'message': str(e)}, 500

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
