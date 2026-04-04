from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.task import Task
import uuid

class TaskRepository:
    def __init__(self, session:AsyncSession):
        self.session = session

    async def create(self,task:Task)->Task:
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task
    
    async def get_tasks(self,skip:int, limit:int,status: str | None):
        statement = select(Task)
        if status:
            statement = statement.where(Task.status == status)
        # Filtering logic here...
        statement = statement.offset(skip).limit(limit)
        result = await self.session.exec(statement)
        return result.all()