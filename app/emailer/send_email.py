import smtplib
from email.message import EmailMessage
from pathlib import Path
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
import os


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# === SMTP CONFIG ===
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

# === JINJA ENV (shared) ===
env = Environment(
    loader=FileSystemLoader(str(BASE_DIR / "templates")),
    autoescape=True,
)


def send_email(
    *,
    to_email: str,
    recipient_name: str,
    template_file: str,
    subject: str,
    sender_name: str,
    position: str
):
    """
    Sends an HTML email using the given Jinja template file.
    CID images are attached for email-client rendering.
    """

    # --- Render template ---
    template = env.get_template(template_file)

    html_content = template.render(
        recipient_name=recipient_name,
        preview_mode=False,  # IMPORTANT: email mode
        sender_name=sender_name,
        position=position
    )

    # --- Build message ---
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{sender_name} <{EMAIL_FROM}>"
    msg["To"] = to_email

    msg.set_content("This email requires an HTML-capable email client.")
    msg.add_alternative(html_content, subtype="html")

    # --- Attach CID images ---
    images = {
        "header_image": BASE_DIR / "assets" / "BigHeader.png",
        "footer_image": BASE_DIR / "assets" / "ICPEPLogo.png",
    }

    html_part = msg.get_body(preferencelist=("html",))
    if html_part is None:
        raise RuntimeError("HTML body was not created")

    for cid, path in images.items():
        with open(path, "rb") as img:
            html_part.add_related(
                img.read(),
                maintype="image",
                subtype=path.suffix.lstrip("."),
                cid=f"<{cid}>",
                filename=path.name,
            )

    # --- Send ---
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
