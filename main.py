from datetime import date, datetime
from fastapi import Depends, FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import re

from pydantic import BaseModel, field_validator
from database import get_db
from models import User
class RegisterForm(BaseModel):
    firstname: str
    surname: str
    dateofbirth: str
    gender: str
    email: str
    password: str

    @field_validator('firstname', 'surname')
    def names_must_be_alpha(cls, v):
        if not re.fullmatch(r'[A-Za-z]+', v):
            raise ValueError('Name must contain only letters')
        return v
app = FastAPI(
    docs_url=None,       # disables /docs
    redoc_url=None,      # disables /redoc
    openapi_url=None     # disables /openapi.json (schema)
)


# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Templates
templates = Jinja2Templates(directory="templates")


@app.get("/register", response_class=HTMLResponse)
def home(request: Request):
    """Home page with speech recognition"""
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def register_user(
    firstname: str = Form(...),
    surname: str = Form(...),
    dateofbirth: str = Form(...),
    gender: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Validate using Pydantic
    try:
        user_data = RegisterForm(
            firstname=firstname,
            surname=surname,
            dateofbirth=dateofbirth,
            gender=gender,
            email=email,
            password=password
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Save to DB
    user = User(
        firstname=user_data.firstname,
        surname=user_data.surname,
        dateofbirth=datetime.strptime(user_data.dateofbirth, "%Y-%m-%d").date(),
        gender=user_data.gender,
        email=user_data.email,
        password=user_data.password  # 🔒 Ideally, hash this
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return RedirectResponse(url="/", status_code=302)




@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Home page with speech recognition"""

    return templates.TemplateResponse("login.html", {"request": request}) 


