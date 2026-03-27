# Task Management System

A comprehensive task management application built with Django REST Framework, featuring role-based access control, task assignment, completion tracking, and detailed reporting capabilities.

## Features

###  Authentication & Authorization
- JWT-based authentication with refresh tokens
- Role-based access control (SuperAdmin, Admin, User)
- Secure password management
- User profile management

###  User Management
- Create, read, update, delete users
- Role assignment and hierarchy
- User statistics and reporting
- Admin can manage assigned users

###  Task Management
- Create and assign tasks with priorities
- Task status tracking (Pending, In Progress, Completed)
- Due date management with overdue detection
- Completion reports with worked hours tracking
- Task filtering and search capabilities

###  Dashboard & Reporting
- Comprehensive dashboard with statistics
- Task completion reports
- User activity tracking
- Priority and status distribution
- Overdue task monitoring

### Admin Panel
- Web-based administration interface
- Modern, responsive design
- Real-time statistics
- Task and user management forms

## Technology Stack

- **Backend**: Django 6.0.3, Django REST Framework
- **Authentication**: JWT (Simple JWT)
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Frontend**: HTML, CSS, JavaScript (Admin Panel)
- **API Documentation**: Comprehensive REST API

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Task-Management-System
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Navigate to source directory**
   ```bash
   cd src
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

The application will be available at:
- API: `http://127.0.0.1:8000/api/`
- Admin Panel: `http://127.0.0.1:8000/admin-panel/`
- Django Admin: `http://127.0.0.1:8000/admin/`

## API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Refresh access token
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile

### User Management
- `GET /api/users/` - List users (with pagination & filtering)
- `POST /api/users/` - Create new user
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user
- `POST /api/users/change-password/` - Change password
- `GET /api/users/stats/` - User statistics

### Task Management
- `GET /api/tasks/` - List tasks (with pagination & filtering)
- `POST /api/tasks/` - Create new task
- `GET /api/tasks/{id}/` - Get task details
- `PUT /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task
- `GET /api/tasks/{id}/report/` - Get completion report
- `GET /api/tasks/stats/` - Task statistics

## User Roles & Permissions

### SuperAdmin
- Full system access
- Manage all users and tasks
- Create admin users
- Delete users
- View all reports

### Admin
- Manage users assigned to them
- Create and assign tasks
- View tasks they created or assigned
- Cannot create SuperAdmin users
- Cannot delete users

### User
- View and update own profile
- View assigned tasks
- Update task status
- Submit completion reports
- Change own password

## Task Workflow

1. **Task Creation**: Admin creates task and assigns to user
2. **Task Assignment**: User receives task in "Pending" status
3. **Task Execution**: User updates status to "In Progress"
4. **Task Completion**: User marks as "Completed" with report and hours
5. **Reporting**: Admin can view completion reports and statistics

## API Usage Examples

### Login
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

### Create Task
```bash
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete documentation",
    "description": "Write API documentation",
    "assigned_to_id": 2,
    "due_date": "2026-04-01",
    "priority": "HIGH"
  }'
```

### Update Task Status
```bash
curl -X PUT http://127.0.0.1:8000/api/tasks/1/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "COMPLETED",
    "completion_report": "Documentation completed successfully",
    "worked_hours": 8.5
  }'
```

## Database Schema

### User Model
- Standard Django User fields
- `role`: SUPERADMIN, ADMIN, USER
- `assigned_admin`: Foreign key to admin user

### Task Model
- `title`, `description`: Task details
- `assigned_to`, `assigned_by`: User relationships
- `due_date`: Task deadline
- `priority`: LOW, MEDIUM, HIGH, URGENT
- `status`: PENDING, IN_PROGRESS, COMPLETED
- `completion_report`: Detailed completion notes
- `worked_hours`: Time spent on task
- Timestamps: `created_at`, `updated_at`, `completed_at`

## Development

### Project Structure
```
src/
├── config/                 # Django settings and configuration
├── authentication/         # JWT authentication app
├── users/                 # User management app
├── tasks/                 # Task management app
├── admin_panel/           # Web admin interface
├── commons/               # Shared utilities
└── templates/             # HTML templates
```

### Running Tests
```bash
python manage.py test
```

### Code Style
The project follows Django and PEP 8 coding standards.

## Deployment

### Environment Variables
Create a `.env` file with:
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=your-database-url
```

### Production Settings
- Use PostgreSQL database
- Configure static files serving
- Set up proper logging
- Enable HTTPS
- Configure CORS for frontend

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the API documentation
- Review the code examples

## Changelog

### Version 1.0.0
- Initial release
- Complete task management system
- Role-based access control
- REST API with JWT authentication
- Web admin panel
- Comprehensive documentation