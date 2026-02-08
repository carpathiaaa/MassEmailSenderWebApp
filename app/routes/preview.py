from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


from app.auth.dependencies import require_login
from app.emailer.templates import EMAIL_TEMPLATES


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get(
    "/preview",
    response_class=HTMLResponse,
    dependencies=[Depends(require_login)],
)
def preview_email(request: Request):
    """
    Renders the email HTML template inside an iframe
    using sample data.
    """

    campaign = request.session.get("campaign")

    if not campaign:
        return HTMLResponse(
            "No campaign data found. Please go back and start again.",
            status_code=400,
        )

    template_key = campaign.get("template")

    if not template_key or template_key not in EMAIL_TEMPLATES:
        return HTMLResponse(
            "Invalid email template selected.",
            status_code=400,
        )

    template_info = EMAIL_TEMPLATES[template_key]


    return templates.TemplateResponse(
        template_info["file"],
        {
            "request": request,
            "recipient_name": "Sample Recipient",
            "sender_name": campaign.get("sender_name"),
            "position": campaign.get("position"),
            "preview_mode": True,
        },
    )

