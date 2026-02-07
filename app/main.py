from fastapi import FastAPI
from contextlib import asynccontextmanager


from app.db.database import init_db
from app.routes.logs import router as logs_router
from app.routes.bulk import router as bulk_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(logs_router)
app.include_router(bulk_router)


@app.get("/")
def root():
    return {"status" : "ok"}

