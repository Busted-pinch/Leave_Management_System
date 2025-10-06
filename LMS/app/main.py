from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app= FastAPI()
# ==============================

templates = Jinja2Templates(directory="app/templates")  # point to your templates folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Home page (login/registration)
@app.get("/", response_class=HTMLResponse)
def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# HR dashboard
@app.get("/hr", response_class=HTMLResponse)
def hr_dashboard(request: Request):
    return templates.TemplateResponse("hr_dashboard.html", {"request": request})

# Import all routers
# NOTE: This assumes the routers are correctly structured in the app/routers directory
from app.routers import (
    Emp_auth,
    Man_auth,
)

app = FastAPI(title="Employee Leave Management System - Unified Backend")

# ==============================
# CORS setup
# ==============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # later restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# Routers
# ==============================
app.include_router(Emp_auth.router)
app.include_router(Man_auth.router)

# ==============================
# Endpoints
# ==============================
#@app.post("/Application", tags=["Application process"])
#def get(request: Application):
#    try:
#    
#        return {
            
#        }
#    except Exception as e:
#        raise HTTPException(status_code=500, detail=str(e))

# ==============================
# Root endpoint
# ==============================
@app.get("/")
def root():
    return {"message": "Employee Leave MAnagement System Unified Backend is running!"}
