from app.repositories.task_repo import TaskRepository
from app.models.task import Task
from app.models.user import User
from app.models.comment import Comment
from fastapi import BackgroundTasks, HTTPException, status
import uuid

#mock email function
def send_email_notification(email:str,task_title:str):
    print(f"Sending email to {email}: You have been assigned to {task_title}")

class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo


    async def create_task(self, task_data, bg_tasks: BackgroundTasks, assignee:User = None):
        new_task = Task(**task_data.model_dump())
        
        # Logic: if assignee is set, send email notification
        if assignee:
            bg_tasks.add_task(send_email_notification, assignee.email, new_task.title)
        return await self.repo.create(new_task)
    
    async def update_task_status(self,task_id:uuid.UUID, update_data):
        task = await self.repo.get_task_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail= "Task not found"
            )
        # update fields dynamically
        data = update_data.model_dump(exclude_unset = True)
        for key, value in data.items():
            setattr(task,key, value)

        updated_task = await self.repo.update(task)
        return updated_task
    

    async def delete_task(self,task_id:uuid.UUID):
        task = await self.repo.get_task_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= "Task not found"
                )
        
        await self.repo.delete(task)
        return {"Ok": True, "message":f"Task with id:{task_id} deleted succesfully"}
    
    async def add_comment(self, task_id: uuid.UUID, user_id: uuid.UUID, content: str):
        # Verify task exists
        task = await self.repo.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
            
        comment = Comment(content=content, task_id=task_id, user_id=user_id)
        return await self.repo.add_comment(comment)
    