from typing import List
import uuid
from fastapi import HTTPException
from app.repositories.project_repo import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectRead
from app.models.project import Project
from app.models.user import User
from fastapi import HTTPException , status

class ProjectService:
    def __init__(self, repo: ProjectRepository):
        self.repo = repo

    async def create_project(self, obj_in: ProjectCreate, current_user: User) -> ProjectRead:
        project_data = obj_in.model_dump()
        project = Project(**project_data)
        project.owner_id = current_user.id

        created = await self.repo.create(project)
        return ProjectRead.model_validate(created)  

    async def get_projects(self,current_user:User, skip: int = 0, limit: int = 10) -> List[ProjectRead]:
        projects = await self.repo.get_all(owner_id=current_user.id, skip=skip, limit=limit)
        return [ProjectRead.from_orm(p) for p in projects]

    async def get_project(self, project_id: uuid.UUID, current_user: User) -> ProjectRead:
        project = await self.repo.get_by_id(project_id, current_user.id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return ProjectRead.model_validate(project)

    async def update_project(self, project_id: uuid.UUID, obj_in: ProjectUpdate, current_user:User) -> ProjectRead:
        updated = await self.repo.update(project_id, obj_in,current_user.id)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        return ProjectRead.model_validate(updated)

    async def delete_project(self, project_id: uuid.UUID, current_user: User) -> dict:
        project = await self.repo.get_by_id(project_id,current_user.id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        if project.creator_id != current_user.id:
            raise HTTPException(status_code=403, detail="Only project creator can delete")
        deleted = await self.repo.delete(project_id)
        return {"message": "Project deleted successfully"}

