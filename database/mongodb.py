from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME

client = MongoClient(MONGO_URI)

db = client[DATABASE_NAME]

students = db["students"]
admins = db["admins"]
complaints = db["complaints"]

print("MongoDB Connected Successfully!")