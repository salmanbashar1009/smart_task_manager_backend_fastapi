from typing import List, Optional
import uuid
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.comment import Comment
from app.schemas.comment import CommentUpdate
from fastapi import HTTPException

class CommentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, comment: Comment) -> Comment:
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return comment

    async def get_by_task_id(self, task_id: uuid.UUID) -> List[Comment]:
        statement = select(Comment).where(Comment.task_id == task_id)
        results = await self.session.exec(statement)
        return results.all()

    async def get_by_id(self, comment_id: uuid.UUID) -> Optional[Comment]:
        statement = select(Comment).where(Comment.id == comment_id)
        result = await self.session.exec(statement)
        return result.one_or_none()

    async def update(self, comment_id: uuid.UUID, obj_in: "CommentUpdate") -> Comment:
        comment = await self.get_by_id(comment_id)
        if not comment:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Comment not found")
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(comment, field, value)
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return comment

    async def delete(self, comment_id: uuid.UUID) -> bool:
        comment = await self.get_by_id(comment_id)
        if comment:
            await self.session.delete(comment)
            await self.session.commit()
            return True
        return False


