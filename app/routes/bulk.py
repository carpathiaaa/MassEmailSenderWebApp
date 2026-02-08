from fastapi import APIRouter, UploadFile, File, Request, BackgroundTasks, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Depends

import csv
from io import TextIOWrapper
from typing import List, Dict


from app.services.bulk_sender import send_bulk_emails_task
from app.auth.dependencies import require_login
from app.emailer.templates import EMAIL_TEMPLATES



router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Temporary in-memory storage (MVP)
PENDING_RECIPIENTS: List[Dict[str, str]] = []


@router.post("/preview-bulk", response_class=HTMLResponse, dependencies=[Depends(require_login)])
def preview_bulk(request: Request, file: UploadFile = File(...), template: str = Form(...), subject: str = Form(...), sender_name: str = Form(...), position: str = Form(...)):
    if template not in EMAIL_TEMPLATES:
        raise ValueError("Invalid template selected")

    request.session["campaign"] = {
    "template": template,
    "subject": subject,
    "sender_name": sender_name,
    "position": position,
}

    global PENDING_RECIPIENTS
    PENDING_RECIPIENTS = []

    reader = csv.DictReader(TextIOWrapper(file.file, encoding="utf-8"))

    for row in reader:
        email = row.get("email")
        name = row.get("name") or "Partner"

        if not email:
            continue

        PENDING_RECIPIENTS.append({
            "email": email.strip(),
            "name": name.strip()
        })

    return templates.TemplateResponse(
        "bulk_preview.html",
        {
            "request": request,
            "count": len(PENDING_RECIPIENTS),
            "sample": PENDING_RECIPIENTS[0] if PENDING_RECIPIENTS else None
        }
    )


@router.post("/confirm-send", response_class=HTMLResponse, dependencies=[Depends(require_login)])
def confirm_send(request: Request, background_tasks: BackgroundTasks):
    if not PENDING_RECIPIENTS:
        return templates.TemplateResponse(
            "send_confirmation.html",
            {
                "request": request,
                "count": 0,
            },
        )

    campaign = request.session.get("campaign")

    if not campaign:
        return HTMLResponse("No campaign data found", status_code=400)

    background_tasks.add_task(
        send_bulk_emails_task,
        PENDING_RECIPIENTS.copy(),
        campaign,
    )


    return templates.TemplateResponse(
        "send_confirmation.html",
        {
            "request": request,
            "count": len(PENDING_RECIPIENTS),
        },
    )
