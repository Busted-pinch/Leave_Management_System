from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.schemas import UserCreateInput, SignupResponse, LoginInput, LoginTokenOutput
from app.services.auth_service import create_user, authenticate_user, get_current_user
from app.db.mongodb import leave_collection, users_collection
from bson import ObjectId
from datetime import datetime

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/api/v1/Man_auth", tags=["Auth"])
Man_router = APIRouter(prefix="/api/v1/Man_Dash", tags=["Dashboard"])

# ==========================
# Manager Signup
# ==========================
@router.post("/Manager_signup", response_model=SignupResponse)
def manager_signup(data: UserCreateInput):
    return create_user(data.name, data.email, data.department, data.password, role="Manager")

# ==========================
# Manager Login
# ==========================
@router.post("/Manager_login", response_model=LoginTokenOutput)
def manager_login(data: LoginInput):
    return authenticate_user(data.email, data.password)

# ==========================
# Current Manager
# ==========================
def get_current_manager(user: dict = Depends(get_current_user)):
    if user.get("role") != "Manager":
        raise HTTPException(status_code=403, detail="Not authorized")
    return user

# ==========================
# Manager Dashboard (HTML)
# ==========================
@Man_router.get("/Manager_Dashboard", response_class=HTMLResponse)
def get_manager_dashboard(request: Request, current_user: dict = Depends(get_current_manager)):
    return templates.TemplateResponse("hr_dashboard.html", {"request": request})

# ==========================
# View all leave requests
# ==========================
@Man_router.get("/leave_requests")
def get_all_leaves(current_user: dict = Depends(get_current_manager)):
    leaves = list(leave_collection.find({}))
    for leave in leaves:
        leave["_id"] = str(leave["_id"])
    return leaves

# =========================
# ✅ Approve Leave
# =========================
@Man_router.post("/approve_leave/{leave_id}")
def approve_leave(leave_id: str, current_user: dict = Depends(get_current_manager)):
    result = leave_collection.update_one({"_id": ObjectId(leave_id)}, {"$set": {"status": "Approved"}})
    if result.modified_count:
        return {"message": "Leave approved successfully!"}
    return {"message": "Leave not found or already processed"}

# =========================
# ✅ Reject Leave
# =========================
@Man_router.post("/reject_leave/{leave_id}")
def reject_leave(leave_id: str, current_user: dict = Depends(get_current_manager)):
    result = leave_collection.update_one({"_id": ObjectId(leave_id)}, {"$set": {"status": "Rejected"}})
    if result.modified_count:
        return {"message": "Leave rejected successfully!"}
    return {"message": "Leave not found or already processed"}


# ==========================
# List all employees
# ==========================
@Man_router.get("/employees")
def get_employees(current_user: dict = Depends(get_current_manager)):
    employees_cursor = users_collection.find({"role": "Employee"})
    employees = []
    for emp in employees_cursor:
        employees.append({
            "employee_id": emp.get("employee_id", "-"),
            "name": emp.get("name", "-"),
            "email": emp.get("email", "-"),
            "department": emp.get("department", "-"),
            "status": emp.get("status", "Active")
        })
    return employees



# ==========================
# Get pending leaves
# ==========================
@Man_router.get("/leave_requests")
def get_all_leaves(current_user: dict = Depends(get_current_manager)):
    leaves_cursor = leave_collection.find({})
    leaves = []
    for lv in leaves_cursor:
        leaves.append({
            "id": str(lv["_id"]),
            "leaveTitle": lv["title"],
            "employee_name": lv["employee_name"],
            "startDate": lv["start_date"].strftime("%Y-%m-%d") if lv.get("start_date") else None,
            "endDate": lv["end_date"].strftime("%Y-%m-%d") if lv.get("end_date") else None,
            "status": lv.get("status", "Pending")
        })
    return leaves


# ==========================
# Manager profile
# ==========================
@router.get("/me")
def get_manager_profile(current_user: dict = Depends(get_current_manager)):
    return current_user
