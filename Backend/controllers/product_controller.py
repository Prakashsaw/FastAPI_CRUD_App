from flask import jsonify, request
from models.product_model import Product
from bson import ObjectId
from utils.schema_validation import validate_json
from schemas.product_schema import create_product_schema, update_product_schema
from utils.generate_unique_key import generate_unique_key
from models.user_model import User

class ProductController:
    @staticmethod
    def create_product(current_user, data):
        try:
            # first check that data is not empty
            if not data:
                return jsonify({"error": "No input data provided"}), 400
            
            # Authorize the user by checking the user exist in the database or not
            email = current_user['email']
            user = User.get_user(email)
            if not user:
                return jsonify({"error": "Unauthorized user!, Can't do this operation!"}), 401
            
            # Create product_id and add to data dictionary
            product_id = generate_unique_key()
            data['product_id'] = product_id

            # Add user_id to the data dictionary
            data['user_id'] = current_user['user_id']

            # print("data 23: ", data)

            # check that data is correct against the create_products_schema
            error = validate_json(create_product_schema, data)
            if error:
                return error
            
            # Now create new product
            product = Product.create_product(current_user["user_id"], data)
            if not product:
                return jsonify({"error": "Internal server error in creating new products!"}), 500
            
            create_product_res = Product.get_product_by_product_id(current_user['user_id'], product_id)
            # print("create_product_res 33: ", create_product_res)
            created_product = {
                "user_id": create_product_res['user_id'],
                "product_id": create_product_res['product_id'],
                "name": create_product_res['name'],
                "description": create_product_res['description'],
                "category": create_product_res['category'],
                "brand": create_product_res['brand'],
                "price": create_product_res['price'],
                "quantity": create_product_res['quantity'],
                "image": create_product_res['image'],
            }
            return jsonify({"message": "Product created successfully", "created_product": created_product}), 201
        except Exception as e:
            return jsonify({"error": "Internal server error -> " + str(e)}), 500

    @staticmethod
    def get_product(current_user, product_id):
        try:
            # Authorize the user by checking the user exist in the database or not
            email = current_user['email']
            user = User.get_user(email)
            if not user:
                return jsonify({"error": "Unauthorized user!, Can't do this operation!"}), 401
            
            product = Product.get_product_by_product_id(current_user['user_id'], product_id)
            if not product:
                return jsonify({"error": "Product not found"}), 404
            
            product_details = {
                "user_id": product['user_id'],
                "product_id": product['product_id'],
                "name": product['name'],
                "description": product['description'],
                "category": product['category'],
                "brand": product['brand'],
                "price": product['price'],
                "quantity": product['quantity'],
                "image": product['image'],
            }
            return jsonify({"message":"Product fetched successfully!", "product_details": product_details}), 200
        except Exception as e:
            return jsonify({"error": "Internal server error -> " + str(e)}), 500
        
    @staticmethod
    def get_all_products(current_user):
        try:
            # Authorize the user by checking the user exist in the database or not
            email = current_user['email']
            user = User.get_user(email)
            if not user:
                return jsonify({"error": "Unauthorized user!, Can't do this operation!"}), 401
            
            products = Product.get_all_products(current_user['user_id'])
            
            products_list = []
            for product in products:
                product_details = {
                    "user_id": product['user_id'],
                    "product_id": product['product_id'],
                    "name": product['name'],
                    "description": product['description'],
                    "category": product['category'],
                    "brand": product['brand'],
                    "price": product['price'],
                    "category": product['category'],
                    "image": product['image'],
                }
                products_list.append(product_details)

            return jsonify({"message": "All Products fetched successfully!", "products": products_list}), 200
        except Exception as e:
            return jsonify({"error": "Internal server error -> " + str(e)}), 500
        
    @staticmethod
    def update_product(current_user, product_id, data):
        try:
            # check that data is not empty
            if not data:
                return jsonify({"error": "No input data provided"}), 400
            
            # Authorize the user by checking the user exist in the database or not
            email = current_user['email']
            user = User.get_user(email)
            if not user:
                return jsonify({"error": "Unauthorized user!, Can't do this operation!"}), 401
            
            # check that data is correct against the update_products_schema
            error = validate_json(update_product_schema, data)
            if error:
                return error
            
            # Now check that product exist in the database or not
            product = Product.get_product_by_product_id(current_user['user_id'], product_id)
            if not product:
                return jsonify({"error": "Product not found!, Can't be update."}), 404
            
            # Now update the product
            product_update_res = Product.update_product(current_user['user_id'], product_id, data)
            if not product_update_res:
                return jsonify({"error": "Internal server error in updating the product!"}), 500
            
            updated_product = Product.get_product_by_product_id(current_user['user_id'], product_id)
            print("updated_product 134: ", updated_product)
            product_details = {
                "user_id": updated_product['user_id'],
                "product_id": updated_product['product_id'],
                "name": updated_product['name'],
                "description": updated_product['description'],
                "category": updated_product['category'],
                "brand": updated_product['brand'],
                "price": updated_product['price'],
                "quantity": updated_product['quantity'],
                "image": updated_product['image']
            }
            return jsonify({"message": "Product updated successfully", "product_details": product_details}), 200

        except Exception as e:
            return jsonify({"error": "Internal server error -> " + str(e)}), 500
        
    @staticmethod
    def delete_product(current_user, product_id):
        try:
            # Authorize the user by checking the user exist in the database or not
            email = current_user['email']
            user = User.get_user(email)
            if not user:
                return jsonify({"error": "Unauthorized user!, Can't do this operation!"}), 401
            
            # Now check that product exist in the database or not
            product = Product.get_product_by_product_id(current_user['user_id'], product_id)
            if not product:
                return jsonify({"error": "Product not found!, Can't be delete."}), 404
            
            # Now delete the product
            product = Product.delete_product(current_user['user_id'], product_id)
            if not product:
                return jsonify({"error": "Internal server error in deleting the product!"}), 500
            
            return jsonify({"message": "Product deleted successfully!"}), 200
        except Exception as e:
            return jsonify({"error": "Internal server error -> " + str(e)}), 500
