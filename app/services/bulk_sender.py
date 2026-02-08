import time
from typing import List, Dict

from app.emailer.send_email import send_email
from app.db.database import log_email
from app.emailer.templates import EMAIL_TEMPLATES


def send_bulk_emails_task(
    recipients: List[Dict[str, str]],
    template_key: str,
) -> None:
    """
    Background task that sends emails one by one
    using the selected email template and logs results.
    """

    if template_key not in EMAIL_TEMPLATES:
        raise ValueError(f"Unknown email template: {template_key}")

    template_info = EMAIL_TEMPLATES[template_key]

    template_file = template_info["file"]
    subject = template_info.get("subject", "Notification")

    for r in recipients:
        try:
            send_email(
                to_email=r["email"],
                recipient_name=r["name"],
                template_file=template_file,
                subject=subject,
            )

            log_email(
                email=r["email"],
                name=r["name"],
                status="sent",
            )

            time.sleep(1)  # rate limit to avoid SMTP throttling

        except Exception as e:
            log_email(
                email=r["email"],
                name=r["name"],
                status="failed",
                error=str(e),
            )
