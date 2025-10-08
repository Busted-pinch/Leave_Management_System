from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.schemas import Man_login_Input, Man_create_Input, Signup_response, Login_TokenOutput
from app.services.auth_service import create_user, authenticate_user, create_access_token
from app.utils.logger import logger  

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/api/v1/Man_auth", tags=["Auth"])


@router.post("/Manager_signup", response_model=Signup_response)
def Emp_signup(data: Man_create_Input):
    logger.info("Manager signup request received for email=%s", data.email)
    if data.password != data.confirmpass:
        logger.warning("Signup failed: Passwords do not match for email=%s", data.email)
        raise HTTPException(status_code=400, detail="Passwords do not match")
    try:
        create_user(data.name, data.email, data.dept, data.password, role='Manager')
        logger.info("Manager registered successfully: %s", data.email)
        return {"message": "Manager registered"}
    except Exception as e:
        logger.error("Signup failed for Manager=%s: %s", data.name, e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/Manager_login", response_model=Login_TokenOutput)
def login(data: Man_login_Input):
    logger.info("Manager Login request received for email=%s", data.email)
    if not authenticate_user(data.email, data.password):
        logger.warning("Login failed for Manager=%s: Invalid credentials", data.email)
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": data.email})
    logger.info("Manager login successful for email=%s", data.email)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/hr_dashboard", response_class=HTMLResponse)
async def get_hr_dashboard(request: Request):
    return templates.TemplateResponse("hr_dashboard.html", {"request": request})
