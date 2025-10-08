import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from passlib.context import CryptContext
from jose import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from bson import ObjectId
from app.db.mongodb import users_collection, leave_collection, db

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# ==========================
# Password utils
# ==========================
def hash_password(password: str) -> str:
    return pwd_context.hash(password[:72])

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# ==========================
# JWT utils
# ==========================
def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ==========================
# Current user
# ==========================
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_token(token)
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "user_id": str(user["_id"]),
        "employee_id": user.get("employee_id"),
        "name": user["name"],
        "email": user["email"],
        "department": user["department"],
        "role": user.get("role", "Employee")
    }

# ==========================
# Employee ID generator
# ==========================
def get_next_employee_number():
    counter = db.counters.find_one_and_update(
        {"_id": "employee_number"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True
    )
    return f"EMP{counter['seq']:03d}"

# ==========================
# User creation
# ==========================
def create_user(name: str, email: str, department: str, password: str, role: str = "Employee"):
    # 1️⃣ Check email uniqueness
    if users_collection.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2️⃣ Generate Employee ID if Employee
    employee_id = get_next_employee_number() if role == "Employee" else None

    # 3️⃣ Insert into DB
    user_doc = {
        "name": name,
        "email": email,
        "department": department,
        "password": hash_password(password),
        "role": role
    }
    if employee_id:
        user_doc["employee_id"] = employee_id

    result = users_collection.insert_one(user_doc)

    # 4️⃣ Prepare user info
    user_info = {
        "user_id": str(result.inserted_id),
        "employee_id": employee_id,
        "name": name,
        "email": email,
        "department": department,
        "role": role
    }

    # 5️⃣ Generate token after successful insert
    access_token = create_access_token({
        "user_id": user_info["user_id"],
        "email": email,
        "role": role
    })

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_info
    }

# ==========================
# Authenticate user
# ==========================
def authenticate_user(email: str, password: str):
    user = users_collection.find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    user_info = {
        "user_id": str(user["_id"]),
        "employee_id": user.get("employee_id"),
        "name": user["name"],
        "email": user["email"],
        "department": user["department"],
        "role": user.get("role", "Employee")
    }

    return {
        "access_token": create_access_token({
            "user_id": user_info["user_id"],
            "email": user_info["email"],
            "role": user_info["role"]
        }),
        "token_type": "bearer",
        "user": user_info
    }

# ==========================
# Leave submission
# ==========================
def submit_leave(employee_id: str, employee_name: str, employee_email: str, employee_dept: str,
                 leaveTitle: str, startDate: str, endDate: str, days: int, description: str,
                 status: str = "Pending", icon: str = "📝"):

    leave_doc = {
        "employee_id": employee_id,
        "employee_name": employee_name,
        "employee_email": employee_email,
        "employee_dept": employee_dept,
        "title": leaveTitle,
        "start_date": datetime.strptime(startDate, "%Y-%m-%d"),
        "end_date": datetime.strptime(endDate, "%Y-%m-%d"),
        "days": days,
        "description": description,
        "status": status,
        "icon": icon,
        "applied_on": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    result = leave_collection.insert_one(leave_doc)
    leave_doc["_id"] = str(result.inserted_id)
    return leave_doc
