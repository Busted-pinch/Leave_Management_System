from pydantic import BaseModel, EmailStr
from typing import Optional

# Reusable user create input
class UserCreateInput(BaseModel):
    name: str
    email: EmailStr
    department: str
    password: str

class UserData(BaseModel):
    user_id: Optional[str]
    employee_id: Optional[str]
    name: str
    email: EmailStr
    department: str
    role: Optional[str] = "Employee"

class SignupResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserData

class LoginInput(BaseModel):
    email: EmailStr
    password: str

class LoginTokenOutput(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LeaveRequest(BaseModel):
    leaveTitle: str
    startDate: str
    endDate: str
    days: int
    description: str
