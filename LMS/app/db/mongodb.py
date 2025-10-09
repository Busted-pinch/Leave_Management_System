from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["leave_management"]  # database name

# collections
users_collection = db["users"]
leave_collection = db["leave_applications"]
leave_collection_history = db["leave_history"]