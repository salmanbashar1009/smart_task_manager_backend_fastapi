from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from ..schemas import user
from app.core.database import get_session
from ..repositories import user_repo
from ..services import auth_service

router = APIRouter()

@router.post("/register", response_model= user.UserRead)
async def register(data:user.UserCreate, session: AsyncSession = Depends(get_session)):
    repo  = user_repo.UserRepository(session)
    service = auth_service.AuthService(repo)
    try:
        user = await service.register_user(data.email, data.password)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/login", response_model=user.Token)
async def login(data: user.UserCreate, session: AsyncSession=Depends(get_session)):
    repo = user_repo.UserRepository(session)
    service = auth_service.AuthService(repo)
    try:
        user = await service.login_user(data.email, data.password)
        return user
    except ValueError:
        raise HTTPException(status_code=401, detail='Invalid credentials')