from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import UserCreateInput, SignupResponse, LoginInput, LoginTokenOutput, LeaveRequest
from app.services.auth_service import create_user, authenticate_user, submit_leave, get_current_user
from app.db.mongodb import leave_collection, leave_collection_history, users_collection
from bson import ObjectId
router = APIRouter(prefix="/api/v1/Emp_auth", tags=["Auth"])
Emp_router = APIRouter(prefix="/api/v1/Emp_Dash", tags=["Dashboard"])

# ==========================
# Current Employee
# ==========================
def get_current_employee(user: dict = Depends(get_current_user)):
    if user.get("role") != "Employee":
        raise HTTPException(status_code=403, detail="Not authorized")
    return user

# ==========================
# Employee Signup & Login
# ==========================
@router.post("/Employee_signup", response_model=SignupResponse)
def employee_signup(data: UserCreateInput):
    try:
        user = create_user(**data.dict(), role="Employee")
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


@router.post("/Employee_login", response_model=LoginTokenOutput)
def employee_login(data: LoginInput):
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
# Submit Leave
# ==========================
@Emp_router.post("/submit")
def submit_leave_endpoint(data: LeaveRequest, current_user: dict = Depends(get_current_employee)):
    leave_doc = submit_leave(
        employee_id=current_user.get("employee_id", "Unknown"),
        employee_name=current_user.get("name", "Unknown"),
        employee_email=current_user.get("email", ""),
        employee_dept=current_user.get("department", ""),
        leaveTitle=data.leaveTitle or "Untitled Application",
        startDate=data.startDate,
        endDate=data.endDate,
        days=data.days or 1,
        description=data.description or ""
    )
    # Convert Mongo _id to string for frontend
    leave_doc["_id"] = str(leave_doc.get("_id"))
    return {"message": "Leave submitted", "leave": leave_doc}

# ==========================
# Get My Leaves
# ==========================
@Emp_router.get("/my_leaves")
def get_my_leaves(current_user: dict = Depends(get_current_employee)):
    active_leaves = list(leave_collection.find({"employee_id": current_user["employee_id"]}))
    history_leaves = list(leave_collection_history.find({"employee_id": current_user["employee_id"]}))
    all_leaves = active_leaves + history_leaves

    leaves = []
    for lv in all_leaves:
        start = lv.get("start_date")
        end = lv.get("end_date")
        leaves.append({
            "leaveId": str(lv.get("_id")),
            "leaveTitle": lv.get("title", "Untitled Application"),
            "startDate": start.strftime("%Y-%m-%d") if start else "",
            "endDate": end.strftime("%Y-%m-%d") if end else "",
            "days": lv.get("days") or 1,
            "description": lv.get("description", ""),
            "status": lv.get("status", "Pending")
        })
    return leaves

# ==========================
# Employee Profile
# ==========================
@router.get("/me")
def get_employee_profile(current_user: dict = Depends(get_current_employee)):
    return {
        "user_id": current_user.get("user_id"),
        "employee_id": current_user.get("employee_id"),
        "name": current_user.get("name", "Unknown"),
        "email": current_user.get("email", ""),
        "department": current_user.get("department", "")
    }
