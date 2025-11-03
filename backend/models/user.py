"""
MongoDB User Model
Stores user authentication and profile information
"""

from typing import Optional, Dict
from datetime import datetime
from bson import ObjectId
from utils.auth import hash_password, verify_password
from utils.database import get_users_collection


class User:
    """User model for MongoDB"""
    
    def __init__(self, username: str, email: str, hashed_password: str, _id: ObjectId = None, created_at: datetime = None):
        self._id = _id or ObjectId()
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self, include_id: bool = False):
        """Convert user to dictionary"""
        data = {
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat()
        }
        if include_id:
            data["_id"] = str(self._id)
        return data
    
    def to_mongo_dict(self):
        """Convert to MongoDB document format"""
        return {
            "_id": self._id,
            "username": self.username,
            "email": self.email,
            "hashed_password": self.hashed_password,
            "created_at": self.created_at
        }
    
    @staticmethod
    def from_mongo_dict(doc: dict):
        """Create User from MongoDB document"""
        if not doc:
            return None
        return User(
            username=doc["username"],
            email=doc["email"],
            hashed_password=doc["hashed_password"],
            _id=doc["_id"],
            created_at=doc.get("created_at", datetime.utcnow())
        )


async def create_user(username: str, email: str, password: str) -> Optional[User]:
    """Create a new user in MongoDB"""
    collection = get_users_collection()
    
    # Check if user already exists
    existing_user = await collection.find_one({"$or": [{"username": username}, {"email": email}]})
    if existing_user:
        return None  # User already exists
    
    # Create new user
    hashed_password = hash_password(password)
    user = User(username, email, hashed_password)
    
    # Insert into MongoDB
    result = await collection.insert_one(user.to_mongo_dict())
    user._id = result.inserted_id
    
    return user


async def get_user(username: str) -> Optional[User]:
    """Get user by username from MongoDB"""
    collection = get_users_collection()
    user_doc = await collection.find_one({"username": username})
    return User.from_mongo_dict(user_doc)


async def get_user_by_id(user_id: str) -> Optional[User]:
    """Get user by ID from MongoDB"""
    collection = get_users_collection()
    try:
        user_doc = await collection.find_one({"_id": ObjectId(user_id)})
        return User.from_mongo_dict(user_doc)
    except:
        return None


async def authenticate_user(username: str, password: str) -> Optional[User]:
    """Authenticate a user with username and password"""
    user = await get_user(username)
    
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user
