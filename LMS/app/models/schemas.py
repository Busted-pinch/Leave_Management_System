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
    employee_id: Optional[str]  # now optional
    manager_id: Optional[str]   # add manager_id
    name: str
    email: EmailStr
    dept: str
    role: str = "employee"


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
    user: Optional[UserData]  # include user details


class LeaveRequest(BaseModel):
    leaveTitle: str
    startDate: str
    endDate: str
    days: int
    description: str
