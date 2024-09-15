from configuration.db_config import users_collection
from datetime import datetime

# User model:  Make sure I am using mongodb database and for that I already creatd database and collections which are in config_database
class User:
    # Method for creating a new user (signup): User Authorization not required
    @staticmethod
    def signup_user(user_id, name, email, password):
        return users_collection.insert_one({"user_id": user_id, "name": name, "email": email, "password": password, "created_at": str(datetime.now()), "updated_at": str(datetime.now())})
        
    # Method for login user: take email and password as input: User Authorization not required
    @staticmethod
    def login_user(email, password):
        return users_collection.find_one({"email": email, "password": password})
    
    # Method to get user by user_id: User Authorization required
    @staticmethod
    def get_user(email):
        return users_collection.find_one({"email": email})
    
    # Method for updating user details: User Authorization required
    @staticmethod
    def update_user(user_id, name, email):
        return users_collection.update_one({"user_id": user_id}, {"$set": {"name": name, "email": email, "updated_at": str(datetime.now())}})
    
    # Method for deleting user (deleting user account permanently): User Authorization required
    @staticmethod
    def delete_user(user_id):
        return users_collection.delete_one({"user_id": user_id})
    
    # Method for logging out user: User Authorization required
    @staticmethod
    def logout_user():
        return {"status": "Success", "message": "User logged out successfully!"}, 200