from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.db.database import get_connection

router = APIRouter()

@router.get("/logs", response_class=HTMLResponse)
def view_logs():
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT email, name, status, error, created_at
            FROM email_logs
            ORDER BY created_at DESC
            LIMIT 100
            """
        ).fetchall()

    html = "<h2>Email Logs</h2><table border='1' cellpadding='6'>"
    html += "<tr><th>Email</th><th>Name</th><th>Status</th><th>Error</th><th>Time</th></tr>"

    for email, name, status, error, created_at in rows:
        html += f"""
        <tr>
            <td>{email}</td>
            <td>{name or ''}</td>
            <td>{status}</td>
            <td>{error or ''}</td>
            <td>{created_at}</td>
        </tr>
        """

    html += "</table>"
    return html
