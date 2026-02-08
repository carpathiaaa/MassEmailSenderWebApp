from fastapi import FastAPI
from contextlib import asynccontextmanager


from app.db.database import init_db
from app.routes.logs import router as logs_router
from app.routes.bulk import router as bulk_router
from app.routes.auth import router as auth_router
from app.routes.preview import router as preview_router

from app.emailer.templates import EMAIL_TEMPLATES



from fastapi import Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.auth.dependencies import require_login


from starlette.middleware.sessions import SessionMiddleware

import os

templates = Jinja2Templates(directory="app/templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/assets"), name="static")
app.include_router(auth_router)
app.include_router(logs_router)
app.include_router(bulk_router)
app.include_router(preview_router)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "dev-secret-change-me")
)



@app.get("/", response_class=HTMLResponse, dependencies=[Depends(require_login)])
def root(request: Request):
    if not request.session.get("user"):
        return RedirectResponse("/login", status_code=302)
    
    return templates.TemplateResponse(
        "dashboard.html",
        {"request" : request,
         "templates": EMAIL_TEMPLATES,}
    )

