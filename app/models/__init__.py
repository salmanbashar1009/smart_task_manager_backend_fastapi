
from .user import User
from .project import Project
from .task import Task
from .comment import Comment

User.model_rebuild()
Project.model_rebuild()
Task.model_rebuild()
Comment.model_rebuild()

