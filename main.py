from datetime import date
from fastapi import Depends, FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session


from database import get_db
from models import User

app = FastAPI(
    # docs_url=None,       # disables /docs
    # redoc_url=None,      # disables /redoc
    # openapi_url=None     # disables /openapi.json (schema)
)


# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Home page with speech recognition"""
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
async def register_user(
    request: Request,
    firstname: str = Form(...),
    surname: str = Form(...),
    dateofbirth: date = Form(...),
    gender: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Create new user with plain text password (⚠️ not safe for real apps)
    new_user = User(
        firstname=firstname,
        surname=surname,
        dateofbirth=dateofbirth,
        gender=gender.lower(),
        email=email,
        password=password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Redirect back to form (you could change this to /login)
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
def home(request: Request):
    """Home page with speech recognition"""

    return templates.TemplateResponse("login.html", {"request": request}) 

