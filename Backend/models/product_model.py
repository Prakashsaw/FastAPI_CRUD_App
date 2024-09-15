from configuration.db_config import products_collection
from datetime import datetime

class Product:
    @staticmethod
    def create_product(user_id, data):
        product = {
            "user_id": user_id,
            "product_id": data['product_id'],
            "name": data['name'],
            "description": data['description'],
            "category": data['category'],
            "brand": data['brand'],
            "price": data['price'],
            "quantity": data['quantity'],
            "image": data['image'],
            "created_at": str(datetime.now()),
            "updated_at": str(datetime.now())
        }
        return products_collection.insert_one(product)

    @staticmethod
    def get_product_by_product_id(user_id, product_id):
        return products_collection.find_one({"user_id": user_id, "product_id": product_id})

    @staticmethod
    def get_all_products(user_id):
        return list(products_collection.find({"user_id": user_id}))

    @staticmethod
    def update_product(user_id, product_id, data):
        return products_collection.update_one(
            {"product_id": product_id, "user_id": user_id},
            {"$set": {
                "name": data['name'],
                "description": data['description'],
                "category": data['category'],
                "brand": data['brand'],
                "price": data['price'],
                "quantity": data['quantity'],
                "image": data['image'],
                "updated_at": str(datetime.now())
            }}
        )

    @staticmethod
    def delete_product(user_id, product_id):
        return products_collection.delete_one({"product_id": product_id, "user_id": user_id})
