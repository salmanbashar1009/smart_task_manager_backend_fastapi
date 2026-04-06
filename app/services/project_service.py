from typing import List
import uuid
from fastapi import HTTPException
from app.repositories.project_repo import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectRead
from app.models.project import Project

class ProjectService:
    def __init__(self, repo: ProjectRepository):
        self.repo = repo

    async def create_project(self, obj_in: ProjectCreate):
        project_data = obj_in.model_dump()
        project = Project(**project_data)
        created = await self.repo.create(project)
        return ProjectRead.from_orm(created)  # or created.model_dump() for pydantic v2

    async def get_projects(self, skip: int = 0, limit: int = 10) -> List[ProjectRead]:
        projects = await self.repo.get_all(skip, limit)
        return [ProjectRead.from_orm(p) for p in projects]

    async def get_project(self, project_id: uuid.UUID) -> ProjectRead:
        project = await self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return ProjectRead.from_orm(project)

    async def update_project(self, project_id: uuid.UUID, obj_in: ProjectUpdate) -> ProjectRead:
        updated = await self.repo.update(project_id, obj_in)
        return ProjectRead.from_orm(updated)

    async def delete_project(self, project_id: uuid.UUID) -> dict:
        deleted = await self.repo.delete(project_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Project not found")
        return {"message": "Project deleted successfully"}

