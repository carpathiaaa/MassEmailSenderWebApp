from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


from app.auth.dependencies import require_login
from app.emailer.templates import EMAIL_TEMPLATES


router = APIRouter()
templates = Jinja2Templates(directory="app/templates/emails")


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

    template_key = request.session.get("selected_template")

    if not template_key or template_key not in EMAIL_TEMPLATES:
        return HTMLResponse(
            "No template selected. Please go back and upload a CSV.",
            status_code=400,
        )

    template_info = EMAIL_TEMPLATES[template_key]

    return templates.TemplateResponse(
        template_info["file"],
        {
            "request": request,
            "recipient_name": "Sample Recipient",
            "preview_mode": True,
            
        },
    )

