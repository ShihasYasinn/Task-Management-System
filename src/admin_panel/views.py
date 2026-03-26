from django.shortcuts import render
from django.http import JsonResponse
from users.models import User
from tasks.models import Task
from tasks.services.task_service import TaskService
from users.services.user_service import UserService


def dashboard(request):
    """Dashboard view with comprehensive statistics"""
    # Get basic counts
    users_count = User.objects.count()
    tasks_count = Task.objects.count()
    
    # Get task status counts
    pending_tasks_count = Task.objects.filter(status='PENDING').count()
    in_progress_tasks_count = Task.objects.filter(status='IN_PROGRESS').count()
    completed_tasks_count = Task.objects.filter(status='COMPLETED').count()
    
    # Get overdue tasks
    from django.utils import timezone
    overdue_tasks_count = Task.objects.filter(
        due_date__lt=timezone.now().date(),
        status__in=['PENDING', 'IN_PROGRESS']
    ).count()
    
    # Get priority distribution
    high_priority_tasks = Task.objects.filter(priority='HIGH').count()
    urgent_priority_tasks = Task.objects.filter(priority='URGENT').count()
    
    # Get recent tasks
    recent_tasks = Task.objects.select_related('assigned_to', 'assigned_by').order_by('-created_at')[:5]
    
    context = {
        "users_count": users_count,
        "tasks_count": tasks_count,
        "pending_tasks_count": pending_tasks_count,
        "in_progress_tasks_count": in_progress_tasks_count,
        "completed_tasks_count": completed_tasks_count,
        "overdue_tasks_count": overdue_tasks_count,
        "high_priority_tasks": high_priority_tasks,
        "urgent_priority_tasks": urgent_priority_tasks,
        "recent_tasks": recent_tasks,
    }
    return render(request, "admin_panel/dashboard.html", context)


def users_list(request):
    """Users list view with enhanced information"""
    users = User.objects.all().order_by('-date_joined')
    
    # Get user statistics
    active_users = users.filter(is_active=True).count()
    inactive_users = users.filter(is_active=False).count()
    admin_users = users.filter(role__in=['ADMIN', 'SUPERADMIN']).count()
    
    context = {
        "users": users,
        "active_users": active_users,
        "inactive_users": inactive_users,
        "admin_users": admin_users,
    }
    return render(request, "admin_panel/users.html", context)


def tasks_list(request):
    """Tasks list view with enhanced filtering"""
    tasks = Task.objects.all().select_related('assigned_to', 'assigned_by').order_by('-created_at')
    
    # Apply filters if provided
    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    
    # Get filter options for the template
    status_choices = Task.STATUS_CHOICES
    priority_choices = Task.PRIORITY_CHOICES
    
    context = {
        "tasks": tasks,
        "status_choices": status_choices,
        "priority_choices": priority_choices,
        "current_status": status_filter,
        "current_priority": priority_filter,
    }
    return render(request, "admin_panel/tasks.html", context)


def task_create(request):
    """Task creation view"""
    if request.method == 'GET':
        users = User.objects.filter(is_active=True).order_by('username')
        priority_choices = Task.PRIORITY_CHOICES
        
        context = {
            "users": users,
            "priority_choices": priority_choices,
        }
        return render(request, "admin_panel/task_create.html", context)
    
    elif request.method == 'POST':
        # Handle task creation
        try:
            # This would typically use the API, but for simplicity, direct model creation
            task = Task.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                assigned_to_id=request.POST.get('assigned_to'),
                due_date=request.POST.get('due_date'),
                priority=request.POST.get('priority', 'MEDIUM'),
            )
            return JsonResponse({'success': True, 'message': 'Task created successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


def user_create(request):
    """User creation view"""
    if request.method == 'GET':
        role_choices = User.ROLE_CHOICES
        admins = User.objects.filter(role__in=['ADMIN', 'SUPERADMIN'])
        
        context = {
            "role_choices": role_choices,
            "admins": admins,
        }
        return render(request, "admin_panel/user_create.html", context)
    
    elif request.method == 'POST':
        # Handle user creation
        try:
            user = User.objects.create_user(
                username=request.POST.get('username'),
                email=request.POST.get('email'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                password=request.POST.get('password'),
                role=request.POST.get('role', 'USER'),
            )
            
            assigned_admin_id = request.POST.get('assigned_admin')
            if assigned_admin_id:
                user.assigned_admin_id = assigned_admin_id
                user.save()
            
            return JsonResponse({'success': True, 'message': 'User created successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})