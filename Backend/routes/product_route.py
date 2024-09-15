from flask import Blueprint, request
from controllers.product_controller import ProductController
from middlewares.user_auth_middleware import token_required

product_routes = Blueprint('product_routes', __name__)

# All routes are protected routes by the token_required middleware (that is user must be logged in to access these routes)
@product_routes.route('/create-product', methods=['POST'])
@token_required
def create_product(current_user):
    data = request.get_json()
    return ProductController.create_product(current_user, data)

@product_routes.route('/get-product/<string:product_id>', methods=['GET'])
@token_required
def get_product(current_user, product_id):
    return ProductController.get_product(current_user, product_id)

@product_routes.route('/get-all-products', methods=['GET'])
@token_required
def get_all_products(current_user):
    return ProductController.get_all_products(current_user)

@product_routes.route('/update-product/<string:product_id>', methods=['PUT'])
@token_required
def update_product(current_user, product_id):
    data = request.get_json()
    return ProductController.update_product(current_user, product_id, data)


@product_routes.route('/delete-product/<string:product_id>', methods=['DELETE'])
@token_required
def delete_product(current_user, product_id):
    return ProductController.delete_product(current_user, product_id)

