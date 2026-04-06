Here’s a cleaner, more structured, and professional rewrite of your API documentation:

---

# 📌 Smart Task Manager – Backend API Documentation

## 🔗 Base URL

```
http://127.0.0.1:8000
```

## 📖 Interactive API Docs

* **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔐 Authentication

All endpoints require **JWT Bearer Token authentication**.

* Include the token in headers:

```
Authorization: Bearer <your_token>
```

* Authentication is handled using:

```
Depends(get_current_user)
```

---

## 🚀 API Overview

### 🔑 Auth Endpoints (`/api/auth/`)

| Method | Endpoint    | Description                            |
| ------ | ----------- | -------------------------------------- |
| POST   | `/register` | Register a new user                    |
| POST   | `/login`    | Authenticate user and return JWT token |

---

### 📁 Project Endpoints (`/api/projects/`)

| Method | Endpoint        | Description                       | Permissions      |
| ------ | --------------- | --------------------------------- | ---------------- |
| POST   | `/`             | Create a new project              | Authenticated    |
| GET    | `/`             | Retrieve all projects (paginated) | Authenticated    |
| GET    | `/{project_id}` | Get project by ID                 | Authenticated    |
| PATCH  | `/{project_id}` | Update project                    | Authenticated    |
| DELETE | `/{project_id}` | Delete project                    | **Creator only** |

**Request Models:**

* `ProjectCreate`: `name (str)`, `description (optional)`
* `ProjectUpdate`

**Response Model:**

* `ProjectRead`

---

### ✅ Task Endpoints (`/api/tasks/`)

| Method | Endpoint     | Description                                | Permissions   |
| ------ | ------------ | ------------------------------------------ | ------------- |
| POST   | `/`          | Create a task (triggers email to assignee) | Authenticated |
| GET    | `/`          | List tasks (supports status filter)        | Authenticated |
| PATCH  | `/{task_id}` | Update task (e.g., status)                 | Authenticated |
| DELETE | `/{task_id}` | Delete a task                              | Authenticated |

**Request Models:**

* `TaskCreate`: `title`, `description?`, `status?`, `project_id?`, `assignee_id?`
* `TaskUpdate`

**Response Model:**

* `TaskRead`

---

### 💬 Comment Endpoints (`/api/tasks/{task_id}/comments/`)

| Method | Endpoint        | Description             | Permissions     |
| ------ | --------------- | ----------------------- | --------------- |
| POST   | `/`             | Add a comment to a task | Authenticated   |
| PATCH  | `/{comment_id}` | Update comment          | **Author only** |
| DELETE | `/{comment_id}` | Delete comment          | **Author only** |

**Request Models:**

* `CommentCreate`: `content (str)`
* `CommentUpdate`

**Response Model:**

* `CommentRead`

---

## 🧩 Data Models (Schemas)

* **User**

  * `id (UUID)`
  * `email`

* **Project**

  * `id`
  * `name`
  * `description`
  * `creator_id`

* **Task**

  * `id`
  * `title`
  * `description`
  * `status`
  * `project_id`
  * `assignee_id`

* **Comment**

  * `id`
  * `content`
  * `task_id`
  * `user_id`
  * `created_at`

---

## ⚠️ Error Handling

| Status Code | Description                             |
| ----------- | --------------------------------------- |
| 401         | Unauthorized (invalid or missing token) |
| 403         | Forbidden (insufficient permissions)    |
| 404         | Resource not found                      |

---

## ✨ Key Features

* 🔒 **Role-based Permissions**

  * Only project creators can delete projects
  * Only comment authors can edit/delete comments

* 📧 **Email Notifications**

  * Mock email sent to assignee upon task creation

* 🗄️ **Database**

  * Built with **SQLModel** and **AsyncPG (PostgreSQL)**

* ⚙️ **Background Tasks**

  * Handles email sending asynchronously

* 🔄 **Auto Reload**

  * Development server reloads automatically on file changes

---

For detailed request/response examples, visit the interactive documentation at `/docs`.
