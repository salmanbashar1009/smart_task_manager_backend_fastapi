from app.repositories.user_repo import UserRepository
from app.models.user import User
from app.core.security import get_hased_password, verify_password, create_access_token

class AuthService:
    def __init__(self,user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, email: str, password: str, role: str = "member"):
        existing_user  = await self.user_repo.get_by_email(email)
        if existing_user:
            raise ValueError("Email already registered")
        
        hashed_pwd = get_hased_password(password)
        user = User(email=email, hashed_password=hashed_pwd, role=role)
        return await self.user_repo.create(user)
    
    async def login_user(self, email:str, password:str):
        user = await self.user_repo.get_by_email(email)

        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")
        
        token = create_access_token({"sub":str(user.id),"role": user.role})

        return {"access_token": token, "token_type": "bearer"}