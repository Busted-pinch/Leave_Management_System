from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.schemas import UserCreateInput, SignupResponse, LoginInput, LoginTokenOutput
from app.services.auth_service import create_user, authenticate_user, get_current_user
from app.db.mongodb import leave_collection, users_collection, leave_collection_history
from bson import ObjectId
from datetime import datetime

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/api/v1/Man_auth", tags=["Auth"])
Man_router = APIRouter(prefix="/api/v1/Man_Dash", tags=["Dashboard"])

# ==========================
# Current Manager
# ==========================
def get_current_manager(user: dict = Depends(get_current_user)):
    if user.get("role") != "Manager":
        raise HTTPException(status_code=403, detail="Not authorized")
    return user

# ==========================
# Manager Signup & Login
# ==========================
@router.post("/Manager_signup", response_model=SignupResponse)
def manager_signup(data: UserCreateInput):
    try:
        user = create_user(**data.dict(), role="Manager")
    except HTTPException as e:
        raise e
    except Exception as e:
        # If partially inserted, remove
        if 'user' in locals() and user.get("user", {}).get("user_id"):
            users_collection.delete_one({"_id": ObjectId(user["user"]["user_id"])})
        raise HTTPException(status_code=500, detail=str(e))

    # Map `department` -> `dept` for Pydantic
    response_user = user["user"].copy()
    response_user["dept"] = response_user.pop("department", "")

    return {
        "access_token": user["access_token"],
        "token_type": user["token_type"],
        "user": response_user
    }



@router.post("/Manager_login", response_model=LoginTokenOutput)
def manager_login(data: LoginInput):
    user = authenticate_user(data.email, data.password)

    # Map `department` -> `dept` for Pydantic
    response_user = user["user"].copy()
    response_user["dept"] = response_user.pop("department", "")

    return {
        "access_token": user["access_token"],
        "token_type": user["token_type"],
        "user": response_user
    }



# ==========================
# Manager Dashboard (HTML)
# ==========================
@Man_router.get("/Manager_Dashboard", response_class=HTMLResponse)
def get_manager_dashboard(request: Request, current_user: dict = Depends(get_current_manager)):
    return templates.TemplateResponse("hr_dashboard.html", {"request": request})

# ==========================
# Approve / Reject Leave
# ==========================
@Man_router.put("/approve_leave/{leave_id}")
def approve_leave(leave_id: str, current_user: dict = Depends(get_current_manager)):
    leave = leave_collection.find_one({"_id": ObjectId(leave_id)})
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    leave["status"] = "Approved"
    leave_collection_history.insert_one(leave)
    leave_collection.delete_one({"_id": ObjectId(leave_id)})

    return {"message": "✅ Leave approved and moved to history"}

@Man_router.put("/reject_leave/{leave_id}")
def reject_leave(leave_id: str, current_user: dict = Depends(get_current_manager)):
    leave = leave_collection.find_one({"_id": ObjectId(leave_id)})
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    leave["status"] = "Rejected"
    leave_collection_history.insert_one(leave)
    leave_collection.delete_one({"_id": ObjectId(leave_id)})

    return {"message": "❌ Leave rejected and moved to history"}

# ==========================
# Leave History (Approved + Rejected)
# ==========================
@Man_router.get("/leave_history")
def get_leave_history(current_user: dict = Depends(get_current_manager)):
    leaves = []
    for lv in leave_collection_history.find({}):
        start = lv.get("start_date")
        end = lv.get("end_date")
        if isinstance(start, datetime): start = start.strftime("%Y-%m-%d")
        if isinstance(end, datetime): end = end.strftime("%Y-%m-%d")

        leaves.append({
            "id": str(lv.get("_id")),
            "leaveTitle": lv.get("title", "Untitled"),
            "employee_name": lv.get("employee_name", "Unknown"),
            "startDate": start or "-",
            "endDate": end or "-",
            "status": lv.get("status", "Unknown")
        })
    return leaves

# ==========================
# Pending Leaves
# ==========================
@Man_router.get("/leave_requests")
def get_pending_leaves(current_user: dict = Depends(get_current_manager)):
    leaves = []
    for lv in leave_collection.find({"status": "Pending"}):
        start = lv.get("start_date")
        end = lv.get("end_date")
        if isinstance(start, datetime): start = start.strftime("%Y-%m-%d")
        if isinstance(end, datetime): end = end.strftime("%Y-%m-%d")

        leaves.append({
            "_id": str(lv.get("_id")),
            "leaveTitle": lv.get("title", "Untitled"),
            "employee_name": lv.get("employee_name", "Unknown"),
            "startDate": start or "",
            "endDate": end or "",
            "status": lv.get("status", "Pending")
        })
    return leaves

# ==========================
# Employees List
# ==========================
@Man_router.get("/employees")
def get_employees(current_user: dict = Depends(get_current_manager)):
    employees = []
    for emp in users_collection.find({"role": "Employee"}):
        employees.append({
            "employee_id": emp.get("employee_id", "Unknown"),
            "name": emp.get("name", "Unknown"),
            "email": emp.get("email", ""),
            "department": emp.get("department", ""),
            "status": emp.get("status", "Active")
        })
    return employees

# ==========================
# All Employee Leaves
# ==========================
@Man_router.get("/employee_leaves")
def get_all_employee_leaves(current_user: dict = Depends(get_current_manager)):
    all_leaves = list(leave_collection.find({})) + list(leave_collection_history.find({}))
    leaves = []

    for lv in all_leaves:
        start = lv.get("start_date")
        end = lv.get("end_date")
        if isinstance(start, datetime): start = start.strftime("%Y-%m-%d")
        if isinstance(end, datetime): end = end.strftime("%Y-%m-%d")

        leaves.append({
            "id": str(lv.get("_id")),
            "employee_name": lv.get("employee_name", "Unknown"),
            "employee_id": lv.get("employee_id", "Unknown"),
            "leaveTitle": lv.get("title", "Untitled"),
            "startDate": start or "-",
            "endDate": end or "-",
            "status": lv.get("status", "Pending")
        })
    return leaves

# ==========================
# Manager Profile
# ==========================
@router.get("/me")
def get_manager_profile(current_user: dict = Depends(get_current_manager)):
    return {
        "user_id": current_user.get("user_id"),
        "manager_id": current_user.get("manager_id", current_user.get("employee_id")),
        "name": current_user.get("name", "Unknown"),
        "email": current_user.get("email", ""),
        "department": current_user.get("department", ""),
        "role": current_user.get("role", "Manager")
    }
