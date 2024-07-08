from pymongo import MongoClient
import os

MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://vedanshiyadav8://add your link')

client = MongoClient(MONGO_URI)
db_name = "gallery"
db = client[db_name]

def init_db():
    try:
        client.admin.command('ping')
        print("MongoDB connection successful!")
        return db
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        exit(1)