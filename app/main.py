from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.core.database import init_db
from .api import auth, task, project

@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.models import User, Project, Task, Comment
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(task.router, prefix="/tasks", tags=["Tasks"])  # ✅ FIX
app.include_router(project.router, prefix="/projects", tags=["Projects"])

@app.get("/")
def root():
    return {"message": "Smart Task Manager Backend - Working"}