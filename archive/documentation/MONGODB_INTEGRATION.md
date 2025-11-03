# MongoDB Integration - Complete Documentation

## Overview

Successfully integrated MongoDB Atlas for persistent user data and daily session storage. The system now stores:
- **User accounts** with bcrypt password hashing
- **Daily mental health sessions** with text, audio, and image analysis results
- **Historical data** for trend analysis

## Database Structure

### Database Name: `mentalhealth`

### Collections

#### 1. **users** Collection
Stores user authentication and profile information.

**Schema:**
```json
{
  "_id": ObjectId,
  "username": "string (unique)",
  "email": "string (unique)",
  "hashed_password": "string (bcrypt)",
  "created_at": "datetime"
}
```

**Indexes:**
- `username` (unique)
- `email` (unique)

#### 2. **sessions** Collection
Stores daily mental health assessment sessions for each user.

**Schema:**
```json
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "username": "string",
  "date": "YYYY-MM-DD",
  "text_analysis": {
    "text": "string",
    "score": 0.0-1.0,
    "bucket": "Low|Moderate|High",
    "explain": {},
    "timestamp": "ISO datetime"
  },
  "audio_analysis": {
    "filename": "string",
    "score": 0.0-1.0,
    "bucket": "Low|Moderate|High",
    "explain": {},
    "timestamp": "ISO datetime"
  },
  "image_analysis": {
    "filename": "string",
    "score": 0.0-1.0,
    "bucket": "Low|Moderate|High",
    "top_emotions": {},
    "explain": {},
    "timestamp": "ISO datetime"
  },
  "fusion_result": {
    "final_score": 0.0-1.0,
    "bucket": "Low|Moderate|High",
    "modality_scores": {},
    "explanation": "string",
    "suggestions": [],
    "timestamp": "ISO datetime"
  },
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**Indexes:**
- `(user_id, date)` - For fast daily session lookups
- `created_at` - For chronological queries

## API Endpoints

### Authentication Endpoints

#### 1. POST `/auth/signup`
Register a new user.

**Request:**
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer",
  "user": {
    "username": "testuser",
    "email": "test@example.com",
    "created_at": "2025-11-03T06:01:10.456208"
  }
}
```

#### 2. POST `/auth/login`
Login with credentials.

**Request:**
```json
{
  "username": "testuser",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer",
  "user": {
    "username": "testuser",
    "email": "test@example.com",
    "created_at": "2025-11-03T06:01:10.456208"
  }
}
```

#### 3. GET `/auth/me`
Get current user info from token.

**Headers:**
```
Authorization: Bearer JWT_TOKEN
```

**Response:**
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "created_at": "2025-11-03T06:01:10.456208"
}
```

### Session-Based Analysis Endpoints

All session endpoints require authentication via `Authorization: Bearer JWT_TOKEN` header.

#### 1. POST `/sessions/analyze/text`
Analyze text and store in daily session.

**Query Parameters:**
- `session_date` (required): YYYY-MM-DD format

**Request:**
```json
{
  "text": "I am feeling stressed and overwhelmed"
}
```

**Response:**
```json
{
  "status": "success",
  "analysis": {
    "score": 0.845,
    "bucket": "High",
    "explain": {}
  },
  "session_id": "SESSION_OBJECT_ID",
  "date": "2025-11-03"
}
```

#### 2. POST `/sessions/analyze/audio`
Analyze audio and store in daily session.

**Query Parameters:**
- `session_date` (optional): YYYY-MM-DD format (defaults to today)

**Request:**
- `file`: Audio file (WAV/MP3/OGG/FLAC/WEBM)

**Response:**
```json
{
  "status": "success",
  "analysis": {
    "score": 0.67,
    "bucket": "Moderate",
    "explain": {}
  },
  "session_id": "SESSION_OBJECT_ID",
  "date": "2025-11-03"
}
```

#### 3. POST `/sessions/analyze/image`
Analyze image and store in daily session.

**Query Parameters:**
- `session_date` (optional): YYYY-MM-DD format (defaults to today)

**Request:**
- `file`: Image file (JPG/PNG)

**Response:**
```json
{
  "status": "success",
  "analysis": {
    "score": 0.45,
    "bucket": "Moderate",
    "top_emotions": {},
    "explain": {}
  },
  "session_id": "SESSION_OBJECT_ID",
  "date": "2025-11-03"
}
```

#### 4. POST `/sessions/aggregate`
Combine all modality scores for a specific date.

**Query Parameters:**
- `session_date` (required): YYYY-MM-DD format

**Response:**
```json
{
  "status": "success",
  "date": "2025-11-03",
  "final_score": 0.72,
  "bucket": "High",
  "modality_scores": {
    "text": 0.845,
    "audio": 0.67,
    "image": 0.45
  },
  "explanation": "Combined analysis from 3 modalities",
  "suggestions": [
    "Consider reaching out to a mental health professional",
    "Practice stress-reduction techniques"
  ]
}
```

#### 5. GET `/sessions/my-sessions`
Get all sessions for current user.

**Query Parameters:**
- `limit` (optional): Number of sessions to return (default: 30)

**Response:**
```json
{
  "username": "testuser",
  "total_sessions": 5,
  "sessions": [
    {
      "_id": "SESSION_ID",
      "user_id": "USER_ID",
      "username": "testuser",
      "date": "2025-11-03",
      "text_analysis": {},
      "audio_analysis": {},
      "image_analysis": {},
      "fusion_result": {},
      "created_at": "2025-11-03T06:01:25.828000",
      "updated_at": "2025-11-03T06:01:25.873000"
    }
  ]
}
```

#### 6. GET `/sessions/{session_date}`
Get a specific session by date.

**Response:**
```json
{
  "_id": "SESSION_ID",
  "user_id": "USER_ID",
  "username": "testuser",
  "date": "2025-11-03",
  "text_analysis": {
    "text": "I am feeling stressed",
    "score": 0.845,
    "bucket": "High",
    "explain": {},
    "timestamp": "2025-11-03T11:31:25.873307"
  },
  "audio_analysis": {},
  "image_analysis": {},
  "fusion_result": {},
  "created_at": "2025-11-03T06:01:25.828000",
  "updated_at": "2025-11-03T06:01:25.873000"
}
```

#### 7. GET `/sessions/range/{start_date}/{end_date}`
Get sessions within a date range.

**Example:** `/sessions/range/2025-11-01/2025-11-30`

**Response:**
```json
{
  "start_date": "2025-11-01",
  "end_date": "2025-11-30",
  "total_sessions": 10,
  "sessions": []
}
```

## Implementation Files

### 1. `backend/utils/database.py`
- MongoDB connection management
- Async Motor client for FastAPI
- Database initialization
- Index creation

### 2. `backend/models/user.py`
- User model with MongoDB integration
- CRUD operations for users
- Password hashing with bcrypt
- User authentication

### 3. `backend/models/session.py`
- Session model for daily entries
- CRUD operations for sessions
- Update methods for each modality
- Date range queries

### 4. `backend/app.py`
- Startup/shutdown events for MongoDB
- Authentication endpoints
- Session-based analysis endpoints
- Helper function for JWT authentication

### 5. `backend/requirements.txt`
Added dependencies:
- `pymongo==4.6.1` - MongoDB driver
- `motor==3.3.2` - Async MongoDB driver

## Configuration

### Environment Variables

Add to `backend/.env`:

```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/mental?retryWrites=true&w=majority
```

Your current MongoDB URI is already configured in `.env`.

## Testing

### Test User Creation
```bash
curl -X POST http://127.0.0.1:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "test1234"}'
```

### Test Session Analysis
```bash
curl -X POST "http://127.0.0.1:8000/sessions/analyze/text?session_date=2025-11-03" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"text": "I am feeling stressed"}'
```

### Test Session Retrieval
```bash
curl -X GET "http://127.0.0.1:8000/sessions/my-sessions" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Features

✅ **User Management:**
- Secure user registration with bcrypt password hashing
- JWT token-based authentication
- User profile retrieval

✅ **Session Storage:**
- Automatic daily session creation
- Separate storage for text, audio, and image analysis
- Update existing sessions without overwriting
- One session per user per day

✅ **Data Persistence:**
- All user data stored in MongoDB Atlas
- Historical session data for trend analysis
- Fast queries with proper indexing

✅ **Professional Structure:**
- User-specific data isolation
- Date-based session organization
- Modality-specific analysis storage
- Combined fusion results

## Next Steps (Optional Enhancements)

1. **Add password reset functionality**
2. **Implement data export (JSON/CSV)**
3. **Add session deletion endpoint**
4. **Implement data analytics dashboard**
5. **Add email verification**
6. **Rate limiting for API endpoints**
7. **Add caching layer (Redis)**

## Status

🎉 **MongoDB Integration Complete!**

- ✅ Database connected: `mentalhealth`
- ✅ Collections created: `users`, `sessions`
- ✅ Indexes configured
- ✅ Authentication working
- ✅ Session storage tested
- ✅ Data retrieval verified

Backend server running on: http://127.0.0.1:8000
