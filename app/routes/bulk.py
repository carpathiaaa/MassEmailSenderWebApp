from fastapi import APIRouter, UploadFile, File, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import csv
from io import TextIOWrapper
from typing import List, Dict

from app.services.bulk_sender import send_bulk_emails_task

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Temporary in-memory storage (MVP)
PENDING_RECIPIENTS: List[Dict[str, str]] = []


@router.post("/preview-bulk", response_class=HTMLResponse)
def preview_bulk(request: Request, file: UploadFile = File(...)):
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


@router.post("/confirm-send")
def confirm_send(background_tasks: BackgroundTasks):
    if not PENDING_RECIPIENTS:
        return {"status": "no recipients to send"}

    # IMPORTANT: copy list so background task is isolated
    background_tasks.add_task(
        send_bulk_emails_task,
        PENDING_RECIPIENTS.copy()
    )

    return {
        "status": "bulk email job started",
        "recipient_count": len(PENDING_RECIPIENTS)
    }
