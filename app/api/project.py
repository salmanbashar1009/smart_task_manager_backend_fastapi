from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
import uuid
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_session
from app.repositories.project_repo import ProjectRepository
from app.services.project_service import ProjectService
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectRead
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

def get_project_service(session: AsyncSession = Depends(get_session)):
    repo = ProjectRepository(session)
    return ProjectService(repo)

@router.post("/", response_model=ProjectRead)
async def create_project(
    data: ProjectCreate, 
    service: ProjectService = Depends(get_project_service),
    current_user: User = Depends(get_current_user)
):
    return await service.create_project(data)

@router.get("/", response_model=List[ProjectRead])
async def list_projects(
    skip: int = Query(0),
    limit: int = Query(10),
    service: ProjectService = Depends(get_project_service),
    current_user: User = Depends(get_current_user)
):
    return await service.get_projects(skip, limit)

@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(
    project_id: str,
    service: ProjectService = Depends(get_project_service),
    current_user: User = Depends(get_current_user)
):
    return await service.get_project(uuid.UUID(project_id))

@router.patch("/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: str,
    data: ProjectUpdate,
    service: ProjectService = Depends(get_project_service),
    current_user: User = Depends(get_current_user)
):
    return await service.update_project(uuid.UUID(project_id), data)

@router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    service: ProjectService = Depends(get_project_service),
    current_user: User = Depends(get_current_user)
):
    return await service.delete_project(uuid.UUID(project_id), current_user)

