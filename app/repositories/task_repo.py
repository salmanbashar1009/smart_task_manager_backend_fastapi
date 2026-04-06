from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.task import Task
from app.models.comment import Comment
import uuid
from typing import Optional


class TaskRepository:
    def __init__(self, session:AsyncSession):
        self.session = session

    async def create(self,task:Task)->Task:
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task
    
    async def get_task_by_id(self,task_id:uuid.UUID)->Task:
        statement = select(Task).where(Task.id == task_id)
        result = await self.session.exec(statement)
        return result.first()
    
    async def get_all(self, skip:int, limit:int, status: Optional[str] = None):
        statement = select(Task)
        if status:
            statement = statement.where(Task.status == status)
        statement = statement.offset(skip).limit(limit)
        result = await self.session.exec(statement)
        return result.all
    
    async def update(self,task:Task)->Task:
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task
    

    async def delete(self, task:Task):
        await self.session.delete(task)
        await self.session.commit()
