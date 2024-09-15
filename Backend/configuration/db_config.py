from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

MONGO_URI = os.getenv("MONGO_URI")

# Create a new client and connect to the server
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Deployment mode :  Successfully connected to MongoDB database!")
except Exception as e:
    print(e)

# Make a connection to a database and create some collections
db = client['Flask_CRUD_App']
users_collection = db['users']
products_collection = db['products']
