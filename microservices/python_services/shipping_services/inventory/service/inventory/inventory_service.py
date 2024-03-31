from extensions import db
from models import Inventory

class InventoryService:

    @staticmethod
    def get_all_inventory_items():
        try:
            items = Inventory.query.all()
            items_list = []
            for item in items:
                item_dict = {column.name: getattr(item, column.name) for column in item.__table__.columns}
                items_list.append(item_dict)
            return {'status': 'success', 'data': items_list}, 200
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500

    @staticmethod
    def list_inventory_items(page=1, per_page=10, query_params=None, order_by='Model', order_direction='desc'):
        try:
            if query_params is None:
                query_params = {}

            # Adapt these variables and filters according to your inventory model attributes
            serial_number = query_params.get('SerialNumber', None)
            model = query_params.get('Model', None)
            condition = query_params.get('Condition', None)

            query = Inventory.query

            if serial_number:
                query = query.filter(Inventory.SerialNumber == serial_number)
            if model:
                query = query.filter(Inventory.Model.like(f"%{model}%"))
            if condition:
                query = query.filter(Inventory.Condition == condition)

            if order_direction == 'desc':
                query = query.order_by(getattr(Inventory, order_by).desc())
            else:
                query = query.order_by(getattr(Inventory, order_by).asc())

            paginated_items = query.paginate(page=page, per_page=per_page, error_out=False)
            items = paginated_items.items

            return {
                'items': [item.to_dict() for item in items],
                'total': paginated_items.total,
                'pages': paginated_items.pages,
                'page': page
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500

    @staticmethod
    def create_inventory_item(data):
        try:
            item = Inventory(**data)
            db.session.add(item)
            db.session.commit()
            return {'status': 'success', 'message': 'Inventory item successfully created.'}, 200
        except Exception as e:
            db.session.rollback()
            return {'status': 'error', 'message': str(e)}, 500

    @staticmethod
    def update_inventory_item(inventory_id, data):
        try:
            item = Inventory.query.filter_by(InventoryID=inventory_id).first()
            if item:
                for key, value in data.items():
                    setattr(item, key, value)
                db.session.commit()
                return {'status': 'success', 'message': 'Inventory item successfully updated.'}, 200
            return {'status': 'error', 'message': 'Inventory item not found.'}, 404
        except Exception as e:
            db.session.rollback()
            return {'status': 'error', 'message': str(e)}, 500

    @staticmethod
    def delete_inventory_item(inventory_id):
        try:
            item = Inventory.query.filter_by(InventoryID=inventory_id).first()
            if item:
                db.session.delete(item)
                db.session.commit()
                return {'status': 'success', 'message': 'Inventory item successfully deleted.'}, 200
            return {'status': 'error', 'message': 'Inventory item not found.'}, 404
        except Exception as e:
            db.session.rollback()
            return {'status': 'error', 'message': str(e)}, 500

    @staticmethod
    def get_inventory_item(inventory_id):
        try:
            item = Inventory.query.filter_by(InventoryID=inventory_id).first()
            if item:
                item_dict = {column.name: getattr(item, column.name) for column in item.__table__.columns}
                return {'status': 'success', 'data': item_dict}, 200
            return {'status': 'error', 'message': 'Inventory item not found.'}, 404
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500
