from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_session
from app.repositories.task_repo import TaskRepository
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, TaskUpdate, TaskRead
from app.schemas.comment import CommentCreate, CommentRead
from app.api.deps import get_current_user, require_admin
from app.models.user import User
from app.repositories.user_repo import UserRepository
from typing import List, Optional

router = APIRouter()

# Helper to inject service
def get_task_service(session: AsyncSession = Depends(get_session)):
    repo = TaskRepository(session)
    return TaskService(repo)

@router.post("/", response_model=TaskRead)
async def create_task(
    data: TaskCreate, 
    background_tasks: BackgroundTasks,
    service: TaskService = Depends(get_task_service),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Check if assignee exists if provided
    assignee = None
    if data.assignee_id:
        user_repo = UserRepository(session)
        assignee = await user_repo.get_by_id(data.assignee_id) # Note: You need to add get_by_id to UserRepo
        
    return await service.create_task(data, background_tasks, assignee)

@router.get("/", response_model=List[TaskRead])
async def list_tasks(
    skip: int = Query(0),
    limit: int = Query(10),
    status: Optional[str] = Query(None),
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user)
):
    # Simple filtering & pagination
    repo = TaskRepository(service.repo.session) # Accessing repo directly for simplicity in this example
    # Ideally service should have a list method
    return await repo.get_all(skip, limit, status)

@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: str,
    data: TaskUpdate,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user)
):
    # Business Logic: Only admins or assignees can update? 
    # For now, we allow any logged-in user for demo.
    return await service.update_task_status(task_id, data)

@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    service: TaskService = Depends(get_task_service),
    # RBAC: Only Admins can delete
    admin_user: User = Depends(require_admin) 
):
    await service.delete_task(task_id)
    return {"message": "Task deleted successfully"}

@router.post("/{task_id}/comments", response_model=CommentRead)
async def add_comment(
    task_id: str,
    data: CommentCreate,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user)
):
    return await service.add_comment(task_id, current_user.id, data.content)