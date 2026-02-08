import time
from typing import List, Dict

from app.emailer.send_email import send_email
from app.db.database import log_email
from app.emailer.templates import EMAIL_TEMPLATES


def send_bulk_emails_task(
    recipients: List[Dict[str, str]],
    campaign: Dict[str, str],
) -> None:
    print("🚀 BULK TASK STARTED")
    print("📦 Campaign:", campaign)
    print("👥 Recipients:", recipients)

    template_key = campaign.get("template")
    subject = campaign.get("subject")
    sender_name = campaign.get("sender_name")
    position = campaign.get("position")

    assert subject is not None
    assert sender_name is not None
    assert position is not None

    print("🧩 Template key:", template_key)
    print("✉️ Subject:", subject)
    print("🧑 Sender:", sender_name)

    if not template_key or template_key not in EMAIL_TEMPLATES:
        print("❌ INVALID TEMPLATE")
        return

    template_file = EMAIL_TEMPLATES[template_key]["file"]

    for r in recipients:
        print("➡️ Sending to:", r)

        try:
            send_email(
                to_email=r["email"],
                recipient_name=r["name"],
                template_file=template_file,
                subject=subject,
                sender_name=sender_name,
                position=position
            )
            print("✅ SENT:", r["email"])

            log_email(
                email=r["email"],
                name=r["name"],
                status="sent",
            )

        except Exception as e:
            print("❌ SEND FAILED:", e)

            log_email(
                email=r["email"],
                name=r["name"],
                status="failed",
                error=str(e),
            )
