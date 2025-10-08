from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.db.mongodb import leave_collection
from app.models.schemas import Emp_login_Input, Emp_create_Input, Signup_response, Login_TokenOutput, LeaveRequest
from app.services.auth_service import create_user, authenticate_user, create_access_token
from app.utils.logger import logger  
from datetime import datetime

router = APIRouter(prefix="/api/v1/Emp_auth", tags=["Auth"])
templates = Jinja2Templates(directory="app/templates")

@router.post("/Employee_signup", response_model=Signup_response)
def Emp_signup(data: Emp_create_Input):
    logger.info("Employee signup request received for email=%s", data.email)
    if data.password != data.confirmpass:
        logger.warning("Signup failed: Passwords do not match for email=%s", data.email)
        raise HTTPException(status_code=400, detail="Passwords do not match")
    try:
        create_user(data.name, data.email, data.dept, data.password, role='Employee')
        logger.info("Employee registered successfully: %s", data.email)
        return {"message": "Employee registered"}
    except Exception as e:
        logger.error("Signup failed for Manager=%s: %s", data.name, e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/Employee_login", response_model=Login_TokenOutput)
def login(data: Emp_login_Input):
    logger.info("Employee Login request received for email=%s", data.email)
    if not authenticate_user(data.email, data.password):
        logger.warning("Login failed for Employee=%s: Invalid credentials", data.email)
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": data.email})
    logger.info("Employee login successful for email=%s", data.email)
    return {"access_token": token, "token_type": "bearer"}

Emp_router = APIRouter(prefix="/api/v1/Emp_dash", tags=["Dashboard"])

@Emp_router.get("/Employee_Dashboard", response_class=HTMLResponse)
async def get_emp_dash(request: Request):
    return templates.TemplateResponse("employee_dashboard.html", {"request": request})

@Emp_router.post("/submit")
async def submit_leave(request: Request, leave: LeaveRequest):
    """
    Handles submission of a leave application by an employee.
    """
    try:
        # Convert dates to datetime objects for DB consistency
        start_date = datetime.strptime(leave.startDate, "%Y-%m-%d")
        end_date = datetime.strptime(leave.endDate, "%Y-%m-%d")

        leave_doc = {
            "employee_id": leave.employee_id,
            "title": leave.leaveTitle,
            "start_date": start_date,
            "end_date": end_date,
            "days": leave.days,
            "description": leave.description,
            "status": leave.status,
            "icon": leave.icon,
            "applied_on": datetime.utcnow()
        }

        result = await leave_collection.insert_one(leave_doc)

        return {"message": "Leave request submitted successfully!", "id": str(result.inserted_id)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@Emp_router.get("/my_leaves")
async def get_my_leaves(employee_id: str):
    leaves = await leave_collection.find({"employee_id": employee_id}).to_list(100)
    return leaves

