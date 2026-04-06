# Smart Task Manager Backend API Documentation

## Base URL
```
http://127.0.0.1:8000
```

## Interactive Docs
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Authentication
- All endpoints require JWT Bearer token (obtained via login).
- Header: `Authorization: Bearer <token>`
- Uses `Depends(get_current_user)` for `current_user: User`.

## API Endpoints

### Auth (assumed /api/auth/)
```
POST /api/auth/register - Create user
POST /api/auth/login - Get JWT token
```

### Projects (/api/projects/)
| Method | Endpoint | Description | Permissions | Request | Response |
|--------|----------|-------------|-------------|---------|----------|
| POST | `/` | Create project | Auth | `ProjectCreate` (name: str, description?: str) | `ProjectRead` |
| GET | `/` | List projects (paginated) | Auth | Query: skip, limit | `List[ProjectRead]` |
| GET | `/{project_id}` | Get project | Auth | - | `ProjectRead` |
| PATCH | `/{project_id}` | Update project | Auth | `ProjectUpdate` | `ProjectRead` |
| **DELETE** | `/{project_id}` | Delete project **(only creator)** | Creator only | - | `{"message": "Project deleted successfully"}` |

### Tasks (/api/tasks/)
| Method | Endpoint | Description | Permissions | Request | Response |
|--------|----------|-------------|-------------|---------|----------|
| POST | `/` | Create task (emails assignee) | Auth | `TaskCreate` (title, description?, status?, project_id?, assignee_id?) | `TaskRead` |
| GET | `/` | List tasks (filter status) | Auth | Query: skip, limit, status | `List[TaskRead]` |
| PATCH | `/{task_id}` | Update task (status etc.) | Auth | `TaskUpdate` | `TaskRead` |
| DELETE | `/{task_id}` | Delete task | Auth | - | `{"message": "..."}` |

### Comments (/api/tasks/{task_id}/comments/)
| Method | Endpoint | Description | Permissions | Request | Response |
|--------|----------|-------------|-------------|---------|----------|
| **POST** | `/{task_id}/comments` | Add comment | Auth | `CommentCreate` (content: str) | `CommentRead` |
| **PATCH** | `/{task_id}/comments/{comment_id}` | Update comment **(only author)** | Author only | `CommentUpdate` (content: str) | `CommentRead` |
| **DELETE** | `/{task_id}/comments/{comment_id}` | Delete comment **(only author)** | Author only | - | `{"message": "Comment deleted successfully"}` |

## Schemas (Pydantic Models)
- **User**: id (UUID), email
- **Project**: id, name, description, creator_id
- **Task**: id, title, description, status, project_id, assignee_id
- **Comment**: id, content, task_id, user_id, created_at

## Error Responses
- 401: Unauthorized
- 403: Forbidden (permissions)
- 404: Not found

## Features
- **Permissions**: Project delete (creator), Comment CRUD (author).
- **Emails**: Mock notification to assignee on task create.
- **Database**: SQLModel + AsyncPG (Postgres).
- **Background Tasks**: Email sending.

Dev server auto-reloads on file changes. See /docs for request/response examples.

