from typing import List, Optional
import uuid
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.project import Project
from app.schemas.project import ProjectUpdate

class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, project_id: uuid.UUID) -> Optional[Project]:
        statement = select(Project).where(Project.id == project_id)
        result = await self.session.exec(statement)
        return result.one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 10) -> List[Project]:
        statement = select(Project).offset(skip).limit(limit)
        results = await self.session.exec(statement)
        return results.all()

    async def create(self, project: Project) -> Project:
        self.session.add(project)
        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def update(self, project_id: uuid.UUID, obj_in: ProjectUpdate) -> Project:
        project = await self.get_by_id(project_id)
        if not project:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Project not found")
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)
        self.session.add(project)
        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def delete(self, project_id: uuid.UUID) -> bool:
        project = await self.get_by_id(project_id)
        if project:
            await self.session.delete(project)
            await self.session.commit()
            return True
        return False

