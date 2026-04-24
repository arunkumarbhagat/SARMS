"""
Run this once to create the default admin user:
  python seed_admin.py
"""
from config import users_collection

users_collection.update_one(
    {"username": "admin"},
    {"$set": {"username": "admin", "password": "admin123", "role": "admin", "ref_id": "admin"}},
    upsert=True
)
print("Admin user created: username=admin, password=admin123")
