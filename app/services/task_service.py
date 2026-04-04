from app.repositories.task_repo import TaskRepository
from app.models.task import Task
from app.models.user import User
from fastapi import BackgroundTasks

def send_email_notification(email:str,task_title:str):
    print(f"Sending email to {email}: You have been assigned to {task_title}")

class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def assign_task(self, task:Task, assignee: User, background_tasks: BackgroundTasks):
        # Business Rule: Check if user is admin or lead (simplified)
        # if current_user.role != "admin": raise PermissionError
        
        task.assignee_id = assignee.id
        updated_task = await self.repo.create(task) # In reality, this would be an update
        
        # Standout Feature: Background Email
        background_tasks.add_task(send_email_notification, assignee.email, task.title)
        return updated_task