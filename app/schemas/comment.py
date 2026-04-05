from pydantic import BaseModel
import uuid


class CommentCreate(BaseModel):
    content: str

class CommentRead(BaseModel):
    id:uuid.UUID
    content: str
    user_id: uuid.UUID
    task_id: uuid.UUID

    class config:
        from_attributes = True