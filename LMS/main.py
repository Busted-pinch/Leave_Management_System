import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# ==============================
# FastAPI app setup
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = FastAPI(title="Employee Leave Management System - Unified Backend")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ==============================
# CORS setup
# ==============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# Import routers
# ==============================
from app.routers import Emp_auth, Man_auth

app.include_router(Emp_auth.router)
app.include_router(Emp_auth.Emp_router)
app.include_router(Man_auth.router)
app.include_router(Man_auth.Man_router)

# ==============================
# HTML Routes (No auth here)
# ==============================
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/employee_dashboard", response_class=HTMLResponse)
def employee_dashboard(request: Request):
    # Page loads regardless of auth
    return templates.TemplateResponse("employee_dashboard.html", {"request": request})

@app.get("/hr_dashboard", response_class=HTMLResponse)
def hr_dashboard(request: Request):
    # Page loads regardless of auth
    return templates.TemplateResponse("hr_dashboard.html", {"request": request})

# ==============================
# Test API
# ==============================
@app.get("/api/v1/test")
def test():
    return {"message": "Unified backend connected successfully!"}
