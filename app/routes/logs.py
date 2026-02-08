from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.db.database import get_connection
from app.auth.dependencies import require_login
from fastapi import Depends

from datetime import datetime
import pytz

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/logs", response_class=HTMLResponse, dependencies=[Depends(require_login)])
def view_logs(request: Request):
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT email, name, status, error, created_at
            FROM email_logs
            ORDER BY created_at DESC
            LIMIT 100
            """
        ).fetchall()

    utc = pytz.utc
    manila = pytz.timezone("Asia/Manila")

    logs = []

    for email, name, status, error, created_at in rows:
        # created_at is an ISO string
        utc_dt = utc.localize(datetime.fromisoformat(created_at))
        local_dt = utc_dt.astimezone(manila)

        logs.append(
            {
                "email": email,
                "name": name,
                "status": status,
                "error": error,
                "created_at": local_dt.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    return templates.TemplateResponse(
        "logs.html",
        {
            "request": request,
            "logs": logs,
        },
    )
