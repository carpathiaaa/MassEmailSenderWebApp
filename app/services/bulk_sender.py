import time
from typing import List, Dict

from app.emailer.send_email import send_invitation_email
from app.db.database import log_email


def send_bulk_emails_task(recipients: List[Dict[str, str]]) -> None:
    """
    Background task that sends emails one by one
    and logs the result to SQLite.
    """
    for r in recipients:
        try:
            send_invitation_email(
                to_email=r["email"],
                recipient_name=r["name"]
            )

            log_email(
                email=r["email"],
                name=r["name"],
                status="sent"
            )

            time.sleep(1)  # rate limit to avoid SMTP throttling

        except Exception as e:
            log_email(
                email=r["email"],
                name=r["name"],
                status="failed",
                error=str(e)
            )
