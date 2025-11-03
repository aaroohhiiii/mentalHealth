"""
MongoDB Session Model
Stores user's daily mental health assessment sessions
Each session contains text, audio, and image analysis results for a specific date
"""

from typing import Optional, Dict, List, Any
from datetime import datetime, date
from bson import ObjectId
from utils.database import get_sessions_collection


class Session:
    """
    Session model representing a user's daily mental health entry
    
    Structure:
    - user_id: Reference to User (ObjectId)
    - username: For easier querying
    - date: Date of the session (YYYY-MM-DD)
    - text_analysis: Text sentiment analysis results
    - audio_analysis: Audio emotion detection results  
    - image_analysis: Image facial expression analysis results
    - fusion_result: Combined multimodal analysis
    - created_at: Timestamp when session was created
    - updated_at: Timestamp when session was last updated
    """
    
    def __init__(
        self,
        user_id: ObjectId,
        username: str,
        session_date: str,
        text_analysis: Optional[Dict] = None,
        audio_analysis: Optional[Dict] = None,
        image_analysis: Optional[Dict] = None,
        fusion_result: Optional[Dict] = None,
        _id: ObjectId = None,
        created_at: datetime = None,
        updated_at: datetime = None
    ):
        self._id = _id or ObjectId()
        self.user_id = user_id
        self.username = username
        self.date = session_date  # Format: "YYYY-MM-DD"
        self.text_analysis = text_analysis or {}
        self.audio_analysis = audio_analysis or {}
        self.image_analysis = image_analysis or {}
        self.fusion_result = fusion_result or {}
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self, include_id: bool = False):
        """Convert session to dictionary for API response"""
        data = {
            "username": self.username,
            "date": self.date,
            "text_analysis": self.text_analysis,
            "audio_analysis": self.audio_analysis,
            "image_analysis": self.image_analysis,
            "fusion_result": self.fusion_result,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
        if include_id:
            data["_id"] = str(self._id)
            data["user_id"] = str(self.user_id)
        return data
    
    def to_mongo_dict(self):
        """Convert to MongoDB document format"""
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "username": self.username,
            "date": self.date,
            "text_analysis": self.text_analysis,
            "audio_analysis": self.audio_analysis,
            "image_analysis": self.image_analysis,
            "fusion_result": self.fusion_result,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @staticmethod
    def from_mongo_dict(doc: dict):
        """Create Session from MongoDB document"""
        if not doc:
            return None
        return Session(
            user_id=doc["user_id"],
            username=doc["username"],
            session_date=doc["date"],
            text_analysis=doc.get("text_analysis", {}),
            audio_analysis=doc.get("audio_analysis", {}),
            image_analysis=doc.get("image_analysis", {}),
            fusion_result=doc.get("fusion_result", {}),
            _id=doc["_id"],
            created_at=doc.get("created_at", datetime.utcnow()),
            updated_at=doc.get("updated_at", datetime.utcnow())
        )


async def create_session(user_id: str, username: str, session_date: str) -> Session:
    """
    Create a new session for a user on a specific date
    If session already exists for that date, return existing session
    """
    collection = get_sessions_collection()
    
    # Check if session already exists for this user and date
    existing_session = await collection.find_one({
        "user_id": ObjectId(user_id),
        "date": session_date
    })
    
    if existing_session:
        return Session.from_mongo_dict(existing_session)
    
    # Create new session
    session = Session(
        user_id=ObjectId(user_id),
        username=username,
        session_date=session_date
    )
    
    result = await collection.insert_one(session.to_mongo_dict())
    session._id = result.inserted_id
    
    return session


async def get_session(user_id: str, session_date: str) -> Optional[Session]:
    """Get a specific session for a user and date"""
    collection = get_sessions_collection()
    
    session_doc = await collection.find_one({
        "user_id": ObjectId(user_id),
        "date": session_date
    })
    
    return Session.from_mongo_dict(session_doc)


async def get_user_sessions(user_id: str, limit: int = 30) -> List[Session]:
    """
    Get all sessions for a user (ordered by date, most recent first)
    Default limit: 30 days
    """
    collection = get_sessions_collection()
    
    cursor = collection.find(
        {"user_id": ObjectId(user_id)}
    ).sort("date", -1).limit(limit)
    
    sessions = []
    async for doc in cursor:
        sessions.append(Session.from_mongo_dict(doc))
    
    return sessions


async def update_session_text(user_id: str, session_date: str, text_analysis: Dict) -> Optional[Session]:
    """Update text analysis for a session"""
    collection = get_sessions_collection()
    
    result = await collection.find_one_and_update(
        {"user_id": ObjectId(user_id), "date": session_date},
        {
            "$set": {
                "text_analysis": text_analysis,
                "updated_at": datetime.utcnow()
            }
        },
        return_document=True
    )
    
    return Session.from_mongo_dict(result)


async def update_session_audio(user_id: str, session_date: str, audio_analysis: Dict) -> Optional[Session]:
    """Update audio analysis for a session"""
    collection = get_sessions_collection()
    
    result = await collection.find_one_and_update(
        {"user_id": ObjectId(user_id), "date": session_date},
        {
            "$set": {
                "audio_analysis": audio_analysis,
                "updated_at": datetime.utcnow()
            }
        },
        return_document=True
    )
    
    return Session.from_mongo_dict(result)


async def update_session_image(user_id: str, session_date: str, image_analysis: Dict) -> Optional[Session]:
    """Update image analysis for a session"""
    collection = get_sessions_collection()
    
    result = await collection.find_one_and_update(
        {"user_id": ObjectId(user_id), "date": session_date},
        {
            "$set": {
                "image_analysis": image_analysis,
                "updated_at": datetime.utcnow()
            }
        },
        return_document=True
    )
    
    return Session.from_mongo_dict(result)


async def update_session_fusion(user_id: str, session_date: str, fusion_result: Dict) -> Optional[Session]:
    """Update fusion result for a session"""
    collection = get_sessions_collection()
    
    result = await collection.find_one_and_update(
        {"user_id": ObjectId(user_id), "date": session_date},
        {
            "$set": {
                "fusion_result": fusion_result,
                "updated_at": datetime.utcnow()
            }
        },
        return_document=True
    )
    
    return Session.from_mongo_dict(result)


async def delete_session(user_id: str, session_date: str) -> bool:
    """Delete a session"""
    collection = get_sessions_collection()
    
    result = await collection.delete_one({
        "user_id": ObjectId(user_id),
        "date": session_date
    })
    
    return result.deleted_count > 0


async def get_sessions_by_date_range(user_id: str, start_date: str, end_date: str) -> List[Session]:
    """Get sessions within a date range"""
    collection = get_sessions_collection()
    
    cursor = collection.find({
        "user_id": ObjectId(user_id),
        "date": {"$gte": start_date, "$lte": end_date}
    }).sort("date", -1)
    
    sessions = []
    async for doc in cursor:
        sessions.append(Session.from_mongo_dict(doc))
    
    return sessions
