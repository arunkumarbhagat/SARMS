from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["sarms_local"]

students_collection = db["students"]
teachers_collection = db["teachers"]
users_collection = db["users"]
attendance_collection = db["attendance"]
marks_collection = db["marks"]
subjects_collection = db["subjects"]
