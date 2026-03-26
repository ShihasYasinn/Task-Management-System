from rest_framework import serializers
from django.utils import timezone
from tasks.models import Task
from users.models import User


class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'role']


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserBasicSerializer(read_only=True)
    assigned_by = UserBasicSerializer(read_only=True)
    is_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'assigned_to', 'assigned_by',
            'due_date', 'priority', 'status', 'completion_report', 
            'worked_hours', 'created_at', 'updated_at', 'completed_at',
            'is_overdue'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'completed_at']


class TaskCreateSerializer(serializers.ModelSerializer):
    assigned_to_id = serializers.IntegerField()
    
    class Meta:
        model = Task
        fields = [
            'title', 'description', 'assigned_to_id', 'due_date', 'priority'
        ]
    
    def validate_assigned_to_id(self, value):
        try:
            user = User.objects.get(id=value)
            if not user.is_active:
                raise serializers.ValidationError("Cannot assign task to inactive user.")
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")
    
    def validate_due_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status', 'completion_report', 'worked_hours']
    
    def validate(self, data):
        status = data.get('status')
        if status == 'COMPLETED':
            if not data.get('completion_report'):
                raise serializers.ValidationError({
                    'completion_report': 'Completion report is required when marking task as completed.'
                })
            if not data.get('worked_hours'):
                raise serializers.ValidationError({
                    'worked_hours': 'Worked hours is required when marking task as completed.'
                })
        return data


class TaskReportSerializer(serializers.ModelSerializer):
    assigned_to = UserBasicSerializer(read_only=True)
    assigned_by = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'assigned_to', 'assigned_by',
            'due_date', 'priority', 'status', 'completion_report', 
            'worked_hours', 'created_at', 'completed_at'
        ]