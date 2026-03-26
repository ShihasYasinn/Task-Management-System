from django.utils import timezone
from django.db.models import Q, Count, Avg
from tasks.models import Task
from users.models import User


class TaskService:

    @staticmethod
    def get_tasks(user, filters=None):
        """Get tasks based on user role and filters"""
        if user.is_superadmin():
            queryset = Task.objects.all()
        elif user.is_admin():
            # Admin can see tasks assigned to users under them
            queryset = Task.objects.filter(
                Q(assigned_to=user) | 
                Q(assigned_to__assigned_admin=user) |
                Q(assigned_by=user)
            )
        else:
            # Regular users can only see their own tasks
            queryset = Task.objects.filter(assigned_to=user)
        
        # Apply filters
        if filters:
            if filters.get('status'):
                queryset = queryset.filter(status=filters['status'])
            if filters.get('priority'):
                queryset = queryset.filter(priority=filters['priority'])
            if filters.get('overdue'):
                queryset = queryset.filter(
                    due_date__lt=timezone.now().date(),
                    status__in=['PENDING', 'IN_PROGRESS']
                )
            if filters.get('search'):
                search_term = filters['search']
                queryset = queryset.filter(
                    Q(title__icontains=search_term) |
                    Q(description__icontains=search_term)
                )
        
        return queryset.select_related('assigned_to', 'assigned_by').order_by('-created_at')

    @staticmethod
    def create_task(user, data):
        """Create a new task (Admin/SuperAdmin only)"""
        if not user.is_admin() and not user.is_superadmin():
            raise Exception("Permission denied. Only admins can create tasks.")
        
        assigned_to = User.objects.get(id=data['assigned_to_id'])
        
        # Admin can only assign to users under them
        if user.is_admin() and assigned_to.assigned_admin != user:
            raise Exception("You can only assign tasks to users under your supervision.")
        
        task = Task.objects.create(
            title=data['title'],
            description=data['description'],
            assigned_to=assigned_to,
            assigned_by=user,
            due_date=data['due_date'],
            priority=data.get('priority', 'MEDIUM')
        )
        
        return task

    @staticmethod
    def update_task(user, task_id, data):
        """Update task status and completion details"""
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise Exception("Task not found")

        # Check permissions
        if not user.is_superadmin():
            if user.is_admin():
                # Admin can update tasks they created or assigned to their users
                if task.assigned_by != user and task.assigned_to.assigned_admin != user:
                    raise Exception("Permission denied")
            else:
                # Regular users can only update their own tasks
                if task.assigned_to != user:
                    raise Exception("Permission denied")

        status = data.get("status")
        
        if status == "COMPLETED":
            report = data.get("completion_report")
            hours = data.get("worked_hours")

            if not report or not hours:
                raise Exception("Completion report and worked hours are required")

            task.completion_report = report
            task.worked_hours = hours
            task.completed_at = timezone.now()

        if status:
            task.status = status
        
        task.save()
        return task

    @staticmethod
    def delete_task(user, task_id):
        """Delete a task (Admin/SuperAdmin only)"""
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise Exception("Task not found")
        
        if not user.is_admin() and not user.is_superadmin():
            raise Exception("Permission denied. Only admins can delete tasks.")
        
        # Admin can only delete tasks they created
        if user.is_admin() and task.assigned_by != user:
            raise Exception("You can only delete tasks you created.")
        
        task.delete()

    @staticmethod
    def get_task_report(user, task_id):
        """Get detailed task report"""
        try:
            task = Task.objects.select_related('assigned_to', 'assigned_by').get(id=task_id)
        except Task.DoesNotExist:
            raise Exception("Task not found")

        # Check permissions
        if not user.is_superadmin():
            if user.is_admin():
                if task.assigned_by != user and task.assigned_to.assigned_admin != user:
                    raise Exception("Permission denied")
            else:
                if task.assigned_to != user:
                    raise Exception("Permission denied")

        return task

    @staticmethod
    def get_dashboard_stats(user):
        """Get dashboard statistics based on user role"""
        if user.is_superadmin():
            tasks = Task.objects.all()
        elif user.is_admin():
            tasks = Task.objects.filter(
                Q(assigned_to__assigned_admin=user) | Q(assigned_by=user)
            )
        else:
            tasks = Task.objects.filter(assigned_to=user)
        
        stats = {
            'total_tasks': tasks.count(),
            'pending_tasks': tasks.filter(status='PENDING').count(),
            'in_progress_tasks': tasks.filter(status='IN_PROGRESS').count(),
            'completed_tasks': tasks.filter(status='COMPLETED').count(),
            'overdue_tasks': tasks.filter(
                due_date__lt=timezone.now().date(),
                status__in=['PENDING', 'IN_PROGRESS']
            ).count(),
            'avg_completion_hours': tasks.filter(
                status='COMPLETED',
                worked_hours__isnull=False
            ).aggregate(avg_hours=Avg('worked_hours'))['avg_hours'] or 0
        }
        
        return stats