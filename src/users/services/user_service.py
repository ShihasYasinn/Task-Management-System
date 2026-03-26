from django.contrib.auth import authenticate
from django.db.models import Q
from users.models import User


class UserService:

    @staticmethod
    def get_users(user, filters=None):
        """Get users based on current user's role and permissions"""
        if user.is_superadmin():
            queryset = User.objects.all()
        elif user.is_admin():
            # Admin can see users assigned to them
            queryset = User.objects.filter(
                Q(assigned_admin=user) | Q(id=user.id)
            )
        else:
            # Regular users can only see themselves
            queryset = User.objects.filter(id=user.id)
        
        # Apply filters
        if filters:
            if filters.get('role'):
                queryset = queryset.filter(role=filters['role'])
            if filters.get('is_active') is not None:
                queryset = queryset.filter(is_active=filters['is_active'])
            if filters.get('search'):
                search_term = filters['search']
                queryset = queryset.filter(
                    Q(username__icontains=search_term) |
                    Q(first_name__icontains=search_term) |
                    Q(last_name__icontains=search_term) |
                    Q(email__icontains=search_term)
                )
        
        return queryset.order_by('-date_joined')

    @staticmethod
    def create_user(current_user, data):
        """Create a new user (Admin/SuperAdmin only)"""
        if not current_user.is_admin() and not current_user.is_superadmin():
            raise Exception("Permission denied. Only admins can create users.")
        
        # Admin can only create users with role USER
        if current_user.is_admin() and data.get('role') != 'USER':
            raise Exception("Admins can only create users with USER role.")
        
        # SuperAdmin can create any role
        if current_user.is_superadmin():
            # If creating an admin, they should be assigned to the current superadmin
            if data.get('role') == 'ADMIN' and not data.get('assigned_admin'):
                data['assigned_admin'] = current_user
        
        # If current user is admin, assign new user to them
        if current_user.is_admin():
            data['assigned_admin'] = current_user
        
        return data

    @staticmethod
    def update_user(current_user, user_id, data):
        """Update user information"""
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Exception("User not found")
        
        # Check permissions
        if not current_user.is_superadmin():
            if current_user.is_admin():
                # Admin can update users assigned to them
                if user.assigned_admin != current_user and user != current_user:
                    raise Exception("Permission denied")
                # Admin cannot change role
                if 'role' in data and data['role'] != user.role:
                    raise Exception("You cannot change user roles")
            else:
                # Regular users can only update themselves (limited fields)
                if user != current_user:
                    raise Exception("Permission denied")
                # Users can only update basic info
                allowed_fields = ['first_name', 'last_name', 'email']
                for field in data.keys():
                    if field not in allowed_fields:
                        raise Exception(f"You cannot update {field}")
        
        # Update user fields
        for field, value in data.items():
            if hasattr(user, field):
                setattr(user, field, value)
        
        user.save()
        return user

    @staticmethod
    def delete_user(current_user, user_id):
        """Delete a user (SuperAdmin only)"""
        if not current_user.is_superadmin():
            raise Exception("Permission denied. Only superadmins can delete users.")
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Exception("User not found")
        
        if user == current_user:
            raise Exception("You cannot delete yourself")
        
        user.delete()

    @staticmethod
    def change_password(user, old_password, new_password):
        """Change user password"""
        if not authenticate(username=user.username, password=old_password):
            raise Exception("Current password is incorrect")
        
        user.set_password(new_password)
        user.save()
        return user

    @staticmethod
    def get_user_stats(current_user):
        """Get user statistics for dashboard"""
        if current_user.is_superadmin():
            users = User.objects.all()
        elif current_user.is_admin():
            users = User.objects.filter(assigned_admin=current_user)
        else:
            users = User.objects.filter(id=current_user.id)
        
        stats = {
            'total_users': users.count(),
            'active_users': users.filter(is_active=True).count(),
            'inactive_users': users.filter(is_active=False).count(),
            'admin_users': users.filter(role='ADMIN').count(),
            'regular_users': users.filter(role='USER').count(),
        }
        
        return stats