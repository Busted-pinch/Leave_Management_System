from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import UserCreateInput, SignupResponse, LoginInput, LoginTokenOutput, LeaveRequest
from app.services.auth_service import create_user, authenticate_user, submit_leave, get_current_user

router = APIRouter(prefix="/api/v1/Emp_auth", tags=["Auth"])
Emp_router = APIRouter(prefix="/api/v1/Emp_Dash", tags=["Dashboard"])

# ==========================
# Employee Signup
# ==========================
@router.post("/Employee_signup", response_model=SignupResponse)
def employee_signup(data: UserCreateInput):
    return create_user(data.name, data.email, data.department, data.password, role="Employee")

# ==========================
# Employee Login
# ==========================
@router.post("/Employee_login", response_model=LoginTokenOutput)
def employee_login(data: LoginInput):
    return authenticate_user(data.email, data.password)

# ==========================
# Current Employee
# ==========================
def get_current_employee(user: dict = Depends(get_current_user)):
    if user.get("role") != "Employee":
        raise HTTPException(status_code=403, detail="Not authorized")
    return user

# ==========================
# Submit Leave
# ==========================
@Emp_router.post("/submit")
def submit_leave_endpoint(data: LeaveRequest, current_user: dict = Depends(get_current_employee)):
    leave_doc = submit_leave(
        employee_id=current_user["employee_id"],
        employee_name=current_user["name"],
        employee_email=current_user["email"],
        employee_dept=current_user["department"],
        leaveTitle=data.leaveTitle,
        startDate=data.startDate,
        endDate=data.endDate,
        days=data.days,
        description=data.description
    )
    return {"message": "Leave submitted", "leave": leave_doc}

# ==========================
# Get my leaves
# ==========================
@Emp_router.get("/my_leaves")
def get_my_leaves(current_user: dict = Depends(get_current_employee)):
    from app.db.mongodb import leave_collection
    leaves_cursor = leave_collection.find({"employee_id": current_user["employee_id"]})
    leaves = []
    for lv in leaves_cursor:
        leaves.append({
            "leaveId": str(lv["_id"]),
            "leaveTitle": lv.get("title"),
            "startDate": lv.get("start_date").strftime("%Y-%m-%d") if lv.get("start_date") else "",
            "endDate": lv.get("end_date").strftime("%Y-%m-%d") if lv.get("end_date") else "",
            "days": lv.get("days"),
            "description": lv.get("description"),
            "status": lv.get("status"),
        })
    return leaves

# ==========================
# Employee profile
# ==========================
@router.get("/me")
def get_employee_profile(current_user: dict = Depends(get_current_employee)):
    return {
        "user_id": current_user["user_id"],
        "employee_id": current_user["employee_id"],
        "name": current_user["name"],
        "email": current_user["email"],
        "department": current_user["department"]
    }
