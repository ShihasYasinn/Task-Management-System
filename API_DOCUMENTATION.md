# Task Management System API Documentation

## Overview
This is a comprehensive Task Management System built with Django REST Framework, featuring role-based access control, task assignment, completion tracking, and reporting capabilities.

## Authentication
The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```

## User Roles
- **SUPERADMIN**: Full system access, can manage all users and tasks
- **ADMIN**: Can manage users assigned to them and create/assign tasks
- **USER**: Can view and update their own tasks

## API Endpoints

### Authentication Endpoints

#### POST /api/auth/login/
Login with username/email and password.

**Request:**
```json
{
    "username": "john_doe",
    "password": "secure_password"
}
```

**Response:**
```json
{
    "success": true,
    "data": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "user": {
            "id": 1,
            "username": "john_doe",
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "role": "USER",
            "is_active": true
        }
    },
    "message": "Login successful"
}
```

#### POST /api/auth/refresh/
Refresh access token using refresh token.

**Request:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### POST /api/auth/logout/
Logout and blacklist refresh token.

**Request:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### GET /api/auth/profile/
Get current user profile information.

### User Management Endpoints

#### GET /api/users/
Get list of users (with pagination and filtering).

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `role`: Filter by role (SUPERADMIN, ADMIN, USER)
- `is_active`: Filter by active status (true/false)
- `search`: Search in username, name, email

**Response:**
```json
{
    "success": true,
    "data": {
        "users": [...],
        "pagination": {
            "current_page": 1,
            "total_pages": 5,
            "total_count": 100,
            "has_next": true,
            "has_previous": false
        }
    }
}
```

#### POST /api/users/
Create a new user (Admin/SuperAdmin only).

**Request:**
```json
{
    "username": "new_user",
    "email": "user@example.com",
    "first_name": "New",
    "last_name": "User",
    "role": "USER",
    "password": "secure_password",
    "password_confirm": "secure_password",
    "assigned_admin": 2
}
```

#### GET /api/users/{id}/
Get user details by ID.

#### PUT /api/users/{id}/
Update user information.

#### DELETE /api/users/{id}/
Delete user (SuperAdmin only).

#### POST /api/users/change-password/
Change current user's password.

**Request:**
```json
{
    "old_password": "current_password",
    "new_password": "new_secure_password",
    "new_password_confirm": "new_secure_password"
}
```

#### GET /api/users/stats/
Get user statistics for dashboard.

### Task Management Endpoints

#### GET /api/tasks/
Get list of tasks (with pagination and filtering).

**Query Parameters:**
- `page`: Page number
- `page_size`: Items per page
- `status`: Filter by status (PENDING, IN_PROGRESS, COMPLETED)
- `priority`: Filter by priority (LOW, MEDIUM, HIGH, URGENT)
- `overdue`: Filter overdue tasks (true/false)
- `search`: Search in title and description

**Response:**
```json
{
    "success": true,
    "data": {
        "tasks": [
            {
                "id": 1,
                "title": "Complete project documentation",
                "description": "Write comprehensive API documentation",
                "assigned_to": {
                    "id": 3,
                    "username": "john_doe",
                    "first_name": "John",
                    "last_name": "Doe",
                    "role": "USER"
                },
                "assigned_by": {
                    "id": 2,
                    "username": "admin",
                    "first_name": "Admin",
                    "last_name": "User",
                    "role": "ADMIN"
                },
                "due_date": "2026-04-01",
                "priority": "HIGH",
                "status": "IN_PROGRESS",
                "completion_report": null,
                "worked_hours": null,
                "created_at": "2026-03-26T10:00:00Z",
                "updated_at": "2026-03-26T10:00:00Z",
                "completed_at": null,
                "is_overdue": false
            }
        ],
        "pagination": {...}
    }
}
```

#### POST /api/tasks/
Create a new task (Admin/SuperAdmin only).

**Request:**
```json
{
    "title": "New Task",
    "description": "Task description",
    "assigned_to_id": 3,
    "due_date": "2026-04-15",
    "priority": "MEDIUM"
}
```

#### GET /api/tasks/{id}/
Get task details by ID.

#### PUT /api/tasks/{id}/
Update task status and completion details.

**Request:**
```json
{
    "status": "COMPLETED",
    "completion_report": "Task completed successfully. All requirements met.",
    "worked_hours": 8.5
}
```

#### DELETE /api/tasks/{id}/
Delete task (Admin/SuperAdmin only).

#### GET /api/tasks/{id}/report/
Get detailed task completion report.

**Response:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "title": "Complete project documentation",
        "description": "Write comprehensive API documentation",
        "assigned_to": {...},
        "assigned_by": {...},
        "due_date": "2026-04-01",
        "priority": "HIGH",
        "status": "COMPLETED",
        "completion_report": "Documentation completed with all API endpoints covered.",
        "worked_hours": 12.5,
        "created_at": "2026-03-26T10:00:00Z",
        "completed_at": "2026-03-28T16:30:00Z"
    }
}
```

#### GET /api/tasks/stats/
Get task statistics for dashboard.

**Response:**
```json
{
    "success": true,
    "data": {
        "total_tasks": 25,
        "pending_tasks": 8,
        "in_progress_tasks": 12,
        "completed_tasks": 5,
        "overdue_tasks": 3,
        "avg_completion_hours": 6.8
    }
}
```

## Task Workflow

### 1. Task Creation
- Admin/SuperAdmin creates a task and assigns it to a user
- Task starts with status "PENDING"
- User receives task assignment

### 2. Task Execution
- User can update task status to "IN_PROGRESS"
- User works on the task
- User can update status back to "PENDING" if needed

### 3. Task Completion
- When marking task as "COMPLETED", user must provide:
  - `completion_report`: Detailed description of work done
  - `worked_hours`: Number of hours spent on the task
- System automatically sets `completed_at` timestamp

### 4. Task Reporting
- Admins and SuperAdmins can view completion reports
- Reports include all task details and completion information
- Statistics are available for dashboard views

## Error Handling

All API endpoints return consistent error responses:

```json
{
    "success": false,
    "error": "Error message",
    "details": {
        "field_name": ["Field-specific error message"]
    }
}
```

Common HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request (validation errors)
- `401`: Unauthorized (authentication required)
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found
- `500`: Internal Server Error

## Permissions

### SuperAdmin
- Full access to all endpoints
- Can create, read, update, delete all users and tasks
- Can assign any role to users

### Admin
- Can manage users assigned to them
- Can create tasks and assign to their users
- Can view and update tasks they created or assigned to their users
- Cannot create SuperAdmin users

### User
- Can view and update their own profile (limited fields)
- Can view tasks assigned to them
- Can update status of their own tasks
- Can provide completion reports for their tasks

## Rate Limiting
API endpoints are protected with rate limiting to prevent abuse. Default limits:
- Authentication endpoints: 5 requests per minute
- Other endpoints: 100 requests per minute per user

## Pagination
List endpoints support pagination with the following parameters:
- `page`: Page number (starts from 1)
- `page_size`: Number of items per page (max 100, default 20)

## Filtering and Search
Most list endpoints support filtering and search:
- Use query parameters to filter results
- Search functionality looks across relevant text fields
- Combine multiple filters for precise results

## Best Practices
1. Always include proper error handling in your client applications
2. Use refresh tokens to maintain user sessions
3. Implement proper logout functionality to blacklist tokens
4. Cache user permissions to reduce API calls
5. Use pagination for large datasets
6. Implement proper loading states in your UI
7. Validate data on the client side before sending to API
8. Handle network errors gracefully