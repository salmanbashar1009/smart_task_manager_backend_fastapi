from typing import List, Optional
import uuid
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.project import Project
from app.schemas.project import ProjectUpdate
from fastapi import HTTPException, status

class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, project_id: uuid.UUID, owner_id: uuid.UUID) -> Optional[Project]:
        """Get project only if it belongs to the owner"""
        statement = select(Project).where(
            Project.id == project_id, 
            Project.owner_id == owner_id
            )
        result = await self.session.exec(statement)
        return result.one_or_none()

    async def get_all(self,owner_id:uuid.UUID, skip: int = 0, limit: int = 10) -> List[Project]:
        """Get only projects belonging to the current user"""
        statement = select(Project).where(
            Project.owner_id == owner_id
        ).offset(skip).limit(limit)
        results = await self.session.exec(statement)
        return results.all()

    async def create(self, project: Project) -> Project:
        self.session.add(project)
        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def update(self, project_id: uuid.UUID,owner_id:uuid.UUID,  obj_in: ProjectUpdate) ->Optional[Project]:
        project = await self.get_by_id(project_id, owner_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)
        self.session.add(project)
        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def delete(self, project_id: uuid.UUID, owner_id: uuid.UUID) -> bool:
        project = await self.get_by_id(project_id, owner_id)
        if project:
            await self.session.delete(project)
            await self.session.commit()
            return True
        return False

