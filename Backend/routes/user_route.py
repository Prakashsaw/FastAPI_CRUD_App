from flask import Blueprint, request
from controllers.user_auth_controller import UserAuthController
from middlewares.user_auth_middleware import token_required

auth_bp = Blueprint('auth', __name__)

# Pullic routes
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    return UserAuthController.signup_user(data)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return UserAuthController.login_user(data)

@auth_bp.route('/logout', methods=['POST'])
def logout():
    return UserAuthController.logout_user()

# Protected routes 

# get user profile route
@auth_bp.route('/user-profile', methods=['GET'])
@token_required
def get_user_profile(current_user):
    return UserAuthController.get_user_profile(current_user)

# user profile update route
@auth_bp.route('/update', methods=['PUT'])
@token_required
def update_user(current_user):
    data = request.get_json()
    return UserAuthController.update_user(current_user, data)

# user delete route
@auth_bp.route('/delete', methods=['DELETE'])
@token_required
def delete_user(current_user):
    return UserAuthController.delete_user(current_user)
