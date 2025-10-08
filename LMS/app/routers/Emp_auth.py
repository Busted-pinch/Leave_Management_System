from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.schemas import Emp_login_Input, Emp_create_Input, Signup_response, Login_TokenOutput
from app.services.auth_service import create_user, authenticate_user, create_access_token
from app.utils.logger import logger  

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


@router.get("/emp_dash", response_class=HTMLResponse)
async def get_emp_dash(request: Request):
    return templates.TemplateResponse("emp_dash.html", {"request": request})
