from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.emailer.send_email import send_invitation_email

app = FastAPI()

@app.get("/")
def root():
    return {"status" : "ok"}

@app.get("/send-test-email")
def send_test_email():
    send_invitation_email(
        to_email="assasinboyugly@gmail.com",
        recipient_name="Juan Dela Cruz"
    )
    return {"status": "email sent"}