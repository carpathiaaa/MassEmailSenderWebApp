import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
from pathlib import Path
from typing import cast

from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SMTP_HOST_RAW = os.getenv("SMTP_HOST")
SMTP_USER_RAW = os.getenv("SMTP_USER")
SMTP_PASSWORD_RAW = os.getenv("SMTP_PASSWORD")
EMAIL_FROM_RAW = os.getenv("EMAIL_FROM")
SMTP_PORT_RAW = os.getenv("SMTP_PORT")

assert SMTP_HOST_RAW is not None, "SMTP_HOST is not set"
assert SMTP_USER_RAW is not None, "SMTP_USER is not set"
assert SMTP_PASSWORD_RAW is not None, "SMTP_PASSWORD is not set"
assert EMAIL_FROM_RAW is not None, "EMAIL_FROM is not set"
assert SMTP_PORT_RAW is not None, "SMTP_PORT is not set"

SMTP_HOST: str = SMTP_HOST_RAW
SMTP_USER: str = SMTP_USER_RAW
SMTP_PASSWORD: str = SMTP_PASSWORD_RAW
EMAIL_FROM: str = EMAIL_FROM_RAW
SMTP_PORT: int = int(SMTP_PORT_RAW)



def send_invitation_email(
        to_email: str,
        recipient_name: str,
):
    env = Environment(
        loader=FileSystemLoader(str(BASE_DIR / "templates")),
        autoescape=True
    )

    template = env.get_template("ga_invitation_email.html")

    html_content = template.render(
        recipient_name=recipient_name,
        sender_name="Charles Chang-il N. Jung"
    )

    msg = EmailMessage()
    msg["Subject"] = "Invitation to Partner – CpE General Assembly 2026"
    msg["From"] = EMAIL_FROM
    msg["To"] = to_email

    msg.set_content(
        "This email requires an HTML-capable email client."
    )


    images = {
        "header_image" : BASE_DIR / "assets" / "BigHeader.png",
        "footer_image" : BASE_DIR / "assets" / "ICPEPLogo.png"
    }

    html_msg = EmailMessage()
    html_msg.set_content(html_content, subtype="html")

    # Attach images as RELATED to the HTML
    for cid, path in images.items():
        with open(path, "rb") as img:
            html_msg.add_related(
                img.read(),
                maintype="image",
                subtype=path.suffix.lstrip("."),
                cid=f"<{cid}>",
                filename=path.name
            )

    # Attach the HTML+images as an alternative
    msg.make_alternative()
    msg.attach(html_msg)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)       