from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os

from app.auth.security import verify_password

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "error": None,
        },
    )

@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    admin_user = os.getenv("ADMIN_USERNAME")
    admin_password_hash = os.getenv("ADMIN_PASSWORD_HASH")

    if (
        username == admin_user
        and admin_password_hash
        and verify_password(password, admin_password_hash)
    ):
        request.session["user"] = username
        return RedirectResponse("/", status_code=302)

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "error": "Invalid username or password",
        },
    )

@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=302)