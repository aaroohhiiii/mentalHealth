"""
MongoDB database connection and configuration
"""
import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

load_dotenv()

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = "mentalhealth"

# Async Motor client for FastAPI async endpoints
motor_client: AsyncIOMotorClient = None
async_db = None

# Synchronous PyMongo client for non-async operations
sync_client: MongoClient = None
sync_db = None


async def connect_to_mongo():
    """
    Establish async connection to MongoDB
    Called on application startup
    """
    global motor_client, async_db
    try:
        motor_client = AsyncIOMotorClient(MONGO_URI)
        async_db = motor_client[DATABASE_NAME]
        
        # Test the connection
        await motor_client.admin.command('ping')
        print(f"✅ Connected to MongoDB (async): {DATABASE_NAME}")
        
        # Create indexes for better performance
        await create_indexes()
        
    except ConnectionFailure as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """
    Close MongoDB connection
    Called on application shutdown
    """
    global motor_client
    if motor_client:
        motor_client.close()
        print("✅ Closed MongoDB connection")


def get_sync_db():
    """
    Get synchronous database connection
    Use this for non-async operations
    """
    global sync_client, sync_db
    if sync_db is None:
        sync_client = MongoClient(MONGO_URI)
        sync_db = sync_client[DATABASE_NAME]
    return sync_db


async def create_indexes():
    """
    Create database indexes for optimized queries
    """
    # User collection indexes
    await async_db.users.create_index("username", unique=True)
    await async_db.users.create_index("email", unique=True)
    
    # Session collection indexes
    await async_db.sessions.create_index([("user_id", 1), ("date", -1)])
    await async_db.sessions.create_index("created_at")
    
    print("✅ Database indexes created")


def get_database():
    """
    Dependency function to get async database
    Use this in FastAPI endpoint dependencies
    """
    return async_db


# Collection helper functions
def get_users_collection():
    """Get users collection (async)"""
    return async_db.users if async_db is not None else None


def get_sessions_collection():
    """Get sessions collection (async)"""
    return async_db.sessions if async_db is not None else None
