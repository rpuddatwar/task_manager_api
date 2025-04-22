# 📝 Task Manager API

A Django RESTful API that allows authenticated users to manage tasks assigned to or created by them, with filtering, pagination, and token-based authentication using JWT.

## 🚀 Tech Stack
- **Framework:** Django
- **Database:** PostgreSQL
- **Authentication:** JWT (djangorestframework-simplejwt)
- **ORM:** Django ORM

## 🔐 User Module
- Login and receive JWT token
- Seed users: `admin_user`, `john_doe`, `jane_smith`

## ✅ Task Module Features
- CRUD operations on tasks
- Tasks have title, description, status, priority, due date, created_at, assigned_by, and assigned_to
- Cannot assign tasks to self
- View tasks assigned **to you** or created **by you**

## 🔎 Filtering Support
- Filter by: `status`, `priority`, `due_before`, `due_after`
- Search by `title` or `description`

## 🔄 Pagination
- Supports `page` and `page_size` query parameters
- Metadata includes total, next, and previous page info

## 📂 Project Structure
- `task_manager/` – Main project
- `users/` – Handles user auth
- `tasks/` – Handles task CRUD

## 🧪 API Usage
Use Postman or any REST client to test with JWT token.
1. Login: `/api/users/token/`
2. Access tasks: `/api/tasks/`

## ⚙️ Setup Instructions
```bash
git clone https://github.com/yourusername/task_manager_api.git
cd task_manager_api
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
