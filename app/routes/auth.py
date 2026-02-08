from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import os

from app.auth.security import verify_password

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
def login_form():
    return """
    <h2>Login</h2>
    <form method="post">
      <input name="username" placeholder="Username" required />
      <input name="password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
    """

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

    return HTMLResponse("Invalid credentials", status_code=302)

@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=302)