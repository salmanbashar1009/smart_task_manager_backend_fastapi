from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.user import User
from typing import Optional

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

        async def get_by_email(self,email:str) -> Optional[User]:
            statement = select(User).where(User.email == email)
            result= await self.session.exec(statement)
            return result.one_or_none()
        
        async def create(self, user: User) -> User:
            self.session.add(user)
            try:
                await self.session.commit()
                await self.session.refresh()
                return user
            except Exception:
                await self.session.rollback()
                raise 
            