from pydantic import BaseModel, EmailStr

class Man_create_Input(BaseModel):
    name: str
    email: EmailStr
    dept: str
    password: str
    confirmpass: str

class Emp_create_Input(BaseModel):
    name: str
    email: EmailStr
    dept: str
    password: str
    confirmpass: str

class Emp_login_Input(BaseModel):
    email: EmailStr
    password: str

class Man_login_Input(BaseModel):
    email: EmailStr
    password: str

class Signup_response(BaseModel):
    message: str

class Login_TokenOutput(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LeaveRequest(BaseModel):
    employee_id: str
    leaveTitle: str
    startDate: str
    endDate: str
    days: int
    description: str
    status: str
    icon: str
