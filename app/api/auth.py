from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from ..schemas import user
from app.core.database import get_session
from ..repositories import user_repo
from ..services import auth_service
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/register", response_model=user.UserRegistrationResponse)
async def register(data: user.UserCreate, session: AsyncSession = Depends(get_session)):
    repo = user_repo.UserRepository(session)
    service = auth_service.AuthService(repo)
    try:
        user = await service.register_user(data.email, data.password)
        return {"success" : True,"message": "user created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=user.Token)
async def login(data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession=Depends(get_session)):
    repo = user_repo.UserRepository(session)
    service = auth_service.AuthService(repo)
    try:
        result = await service.login_user(data.username, data.password)
        return result
    except ValueError:
        raise HTTPException(status_code=401, detail='Invalid credentials')
