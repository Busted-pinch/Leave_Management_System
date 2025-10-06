import os
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from datetime import datetime
from bson import ObjectId
from app.db.mongodb import users_collection, leave_collection
from app.utils.logger import logger

# Load .env file
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password[:72])

def verify_password(plain_password: str, hashed: str) -> bool:
    return pwd_context.verify(plain_password, hashed)

def create_access_token(data: dict):

    to_encode = data.copy()  # Copy payload to avoid mutating original
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Set expiration
    to_encode.update({"exp": expire})  # Add expiration claim
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Encode token

def create_user(name: str, email: str, dept: str, password: str, role: str = "Employee"):
    """
    Create a new user and return a JWT token.
    Returns: dict with 'access_token' and 'token_type'
    Raises: ValueError if email already exists
    """
    if users_collection.find_one({"email": email}):
        logger.warning("Attempt to re-register email: %s", email)
        raise ValueError("Email already registered")

    # Prepare user document
    user_doc = {
        "name": name,
        "email": email,
        "department": dept,
        "password": hash_password(password),
        "role": role
    }

    # Insert into MongoDB
    result = users_collection.insert_one(user_doc)
    logger.info("Created user name=%s email=%s role=%s", name, email, role)

    # ✅ Prepare token payload
    token_data = {
        "user_id": str(result.inserted_id),
        "email": email,
        "role": role
    }

    # ✅ Generate access token
    access_token = create_access_token(token_data)

    # Return token
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ✅ Updated authentication to return JWT token
def authenticate_user(email: str, password: str):
    """
    Authenticate user and return JWT token if successful.
    Returns: dict with 'access_token' and 'token_type'
    Raises: ValueError on failure
    """
    logger.info("Authentication attempt for email=%s", email)
    
    user = users_collection.find_one({"email": email})
    if not user:
        logger.warning("Authentication failed: user not found, email=%s", email)
        raise ValueError("Invalid email or password")
    
    if not verify_password(password, user["password"]):
        logger.warning("Authentication failed: invalid password, email=%s", email)
        raise ValueError("Invalid email or password")
    
    # ✅ Prepare token payload
    token_data = {
        "user_id": str(user["_id"]),  # Include user ID
        "email": user["email"],       # Include email
        "role": user.get("role", "employee")  # Include role, default employee
    }
    
    # ✅ Generate access token
    access_token = create_access_token(token_data)
    
    logger.info("Authentication successful for email=%s", email)
    
    # ✅ Return token in standard format
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

def submit_leave(employee_id: str, subject: str, body: str):
    leave_doc = {
        "employee_id": employee_id,
        "subject": subject,
        "body": body,
        "status": "pending",  # pending, approved, rejected
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    result = leave_collection.insert_one(leave_doc)
    leave_doc["_id"] = str(result.inserted_id)
    return leave_doc

def decide_leave(leave_id: str, decision: str):
    if decision not in ["approved", "rejected"]:
        raise ValueError("Decision must be 'approved' or 'rejected'")

    result = leave_collection.update_one(
        {"_id": ObjectId(leave_id)},
        {"$set": {"status": decision, "updated_at": datetime.utcnow()}}
    )
    if result.matched_count == 0:
        raise ValueError("Leave application not found")
    return True

def get_pending_leaves():
    leaves = []
    cursor = leave_collection.find({"status": "pending"})
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        leaves.append(doc)
    return leaves