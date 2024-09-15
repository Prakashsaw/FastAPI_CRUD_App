from flask import jsonify, session
from models.user_model import User
from utils.generate_unique_key import generate_unique_key
from utils.schema_validation import validate_json
from schemas.user_auth_schema import user_signup_schema, user_login_schema, user_update_schema
from utils.hash_password import hash_password, verify_password
from utils.jwt import create_jwt_token
import re

class UserAuthController:
    @staticmethod
    def signup_user(data):
        try:
            # first check that input data is coming or not and in json format
            if not data:
                return jsonify({"error": "No input data provided"}), 400
            
            # print("data 13: ", data)
            # Add user_id to the data dictionary then go for validation against the schema
            data['user_id'] = generate_unique_key()

            # Validate the input data
            error = validate_json(user_signup_schema, data)
            if error:
                # print("error 27: ", error)
                return error
            
            # check that all the fields are filled can't be empty
            user_id = data['user_id']
            name = data['name']
            email = data['email']
            password = data['password']

            if user_id == "" or name == "" or email == "" or password == "":
                return jsonify({"error": "All fields are required"}), 400
            
            # if email is not in valid format: do it by regex matching
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return jsonify({"error": "Invalid email format"}), 400
            
            # if password is less than 6 characters
            if len(password) < 6:
                return jsonify({"error": "Password must be at least 6 characters"}), 400
            
            # check if user already exists
            user_exist = User.get_user(email)
            # print("user 48: ", user_exist)
            if user_exist:
                return jsonify({"error": "User already exists"}), 409
            
            # Hash the password
            password = data['password']
            hashed_password = hash_password(password)

            # print("data 52: ", data)
            # Create a new user
            user = User.signup_user(data['user_id'], data['name'], data['email'], hashed_password)
            # print("user 62: " , user)
            if not user:
                return jsonify({"error": "Internal server error-> something went wrong in user signed up!"}), 500
            
            created_user = User.get_user(email)
            #  for resolving this error: Object of type InsertOneResult is not JSON serializable, serialize the user object"
            created_user = {"user_id": created_user["user_id"], "name": created_user["name"], "email": created_user["email"]}

            return jsonify({"status": "Success", "message": "User signed up successfully!", "user_details": created_user}), 201
        except Exception as e:
            return jsonify({"error": "Internal server errror -> " + str(e)}), 500
    
    @staticmethod
    def login_user(data):
        try:
            # first check that input data is coming or not and in json format
            if not data:
                return jsonify({"error": "No input data provided"}), 400
            
            # Validate the input data
            error = validate_json(user_login_schema, data)
            if error:
                return error
            
            email = data['email']
            password = data['password']
            
            if email == "" or password == "":
                return jsonify({"error": "All fields are required"}), 400
            
            # check that email is in valid format
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return jsonify({"error": "Invalid email format"}), 400
            
            # check if user exists or not
            user = User.get_user(email)
            if not user:
                return jsonify({"error": "Invalid credentials"}), 401
            
            # Verify the password
            if not verify_password(password, user['password']):
                return jsonify({"error": "Invalid credentials"}), 401
            
            # Pop the password from the user
            # user.pop("password")
            
            # make payload for generate token
            payload = {"user_id": user["user_id"], "email": user["email"]}
            jwt_token = create_jwt_token(payload)
            # print("jwt_token 116: ", jwt_token)

            # Set the user in the session by their user_id
            session['user'] = str(user["user_id"])
            # print("user session 120: ", session)
            #  for resolving this error: Object of type InsertOneResult is not JSON serializable, serialize the user object"
            logged_in_user = {"user_id": user["user_id"], "name": user["name"], "email": user["email"]}

            return jsonify({"status": "Success", "message": "User logged in successfully!", "user_details": logged_in_user, "access_token": jwt_token}), 200
        except Exception as e:
            return jsonify({"error": "Internal server errror -> " + str(e)}), 500
        
    @staticmethod
    def logout_user():
        try:
            session.pop('user', None)
            return jsonify({"status": "Success", "message": "User logged out successfully!"}), 200
        except Exception as e:
            return jsonify({"error": "Internal server errror -> " + str(e)}), 500
        
    @staticmethod
    def get_user_profile(current_user):
        try:
            # check if user exists or not
            user = User.get_user(current_user['email'])
            if not user:
                return jsonify({"error": "User does not exist!"}), 404
            
            #  for resolving this error: Object of type InsertOneResult is not JSON serializable, serialize the user object"
            user = {"user_id": user["user_id"], "name": user["name"], "email": user["email"]}

            return jsonify({"status": "Success", "message": "User profile fetched successfully!", "user_details": user}), 200
        except Exception as e:
            return jsonify({"error": "Internal server errror -> " + str(e)}), 500
        
    @staticmethod
    def update_user(current_user, data):
        try:
            # first check that input data is coming or not and in json format
            if not data:
                return jsonify({"error": "No input data provided"}), 400
            
            print("current_user 13: ", current_user)

            # Validate the input data
            error = validate_json(user_update_schema, data)
            if error:
                # print("error 27: ", error)
                return error
            
            # check that all the fields are filled, can't be empty
            name = data['name']
            email = data['email']

            if name == "" or email == "":
                return jsonify({"error": "All fields are required"}), 400
            
            # if email is not in valid format: do it by regex matching
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return jsonify({"error": "Invalid email format"}), 400
            
            # check that update email given by user is not already exist in database
            user_exist = User.get_user(email)
            if user_exist:
                return jsonify({"error": "This email already taken by someone else!"}), 409
            
            # check if user exists or not, if user exist then update the user details
            authorized_user= User.get_user(current_user['email'])
            
            if not authorized_user:
                return jsonify({"error": "Unauthorized user or token expired, can't be update!"}), 404
            
            # Update the user details
            update_response = User.update_user(current_user['user_id'], data['name'], data['email'])
            print("update_response 181: ", update_response)

            if not update_response:
                return jsonify({"error": "Internal server error-> something went wrong in user updation!"}), 500
            
            updated_user = User.get_user(data['email'])
            #  for resolving this error: Object of type InsertOneResult is not JSON serializable, serialize the user object"
            updated_user = {"user_id": updated_user["user_id"], "name": updated_user["name"], "email": updated_user["email"]}

            return jsonify({"status": "Success", "message": "User details updated successfully!", "updated_user_details": updated_user}), 200
            
        except Exception as e:
            return jsonify({"error": "Internal server errror -> " + str(e)}), 500
        
    @staticmethod
    def delete_user(current_user):
        try:
            # check if user exists or not, if user exist then delete the user
            user = User.get_user(current_user['email'])
            if not user:
                return jsonify({"error": "User does not exist, can't be delete!"}), 404
            
            # Delete the user
            deleted_user = User.delete_user(current_user['user_id'])
            if not deleted_user:
                return jsonify({"error": "Internal server error-> something went wrong in user deletion!"}), 500
            
            return jsonify({"status": "Success", "message": "User deleted successfully!"}), 200
        except Exception as e:
            return jsonify({"error": "Internal server errror -> " + str(e)}), 500