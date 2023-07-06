import configparser
from pymongo import MongoClient
import pymongo

config = configparser.ConfigParser()
config.read('config.txt')

# Construct the MongoDB connection string
mongo_connection_string = f"mongodb://{config.get('database', 'host')}:{config.get('database', 'port')}"

# Establish the connection
client = MongoClient(mongo_connection_string)



# Access the database
db = client[config.get('database', 'db')]

# Test MongoDB connection
try:
    client.server_info()
    print("Connected to MongoDB!")
    # auth.seed_initial_admin_user(mongo_db)
except pymongo.errors.ConnectionFailure:
    print("Failed to connect to MongoDB.")


collection = db["users"]