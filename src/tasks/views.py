from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator

from tasks.services.task_service import TaskService
from tasks.serializers import (
    TaskSerializer, TaskCreateSerializer, TaskUpdateSerializer, TaskReportSerializer
)
from commons.utils.response import APIResponse


class TaskListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get tasks with filtering and pagination"""
        try:
            # Get filter parameters
            filters = {
                'status': request.GET.get('status'),
                'priority': request.GET.get('priority'),
                'overdue': request.GET.get('overdue') == 'true',
                'search': request.GET.get('search'),
            }
            
            # Remove None values
            filters = {k: v for k, v in filters.items() if v is not None and v != ''}
            
            tasks = TaskService.get_tasks(request.user, filters)
            
            # Pagination
            page = request.GET.get('page', 1)
            page_size = request.GET.get('page_size', 20)
            
            paginator = Paginator(tasks, page_size)
            page_obj = paginator.get_page(page)
            
            serializer = TaskSerializer(page_obj.object_list, many=True)
            
            return Response(APIResponse.success(data={
                'tasks': serializer.data,
                'pagination': {
                    'current_page': page_obj.number,
                    'total_pages': paginator.num_pages,
                    'total_count': paginator.count,
                    'has_next': page_obj.has_next(),
                    'has_previous': page_obj.has_previous(),
                }
            }))
        except Exception as e:
            return Response(
                APIResponse.error(str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        """Create a new task (Admin/SuperAdmin only)"""
        try:
            serializer = TaskCreateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    APIResponse.error("Invalid data", serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            task = TaskService.create_task(request.user, serializer.validated_data)
            response_serializer = TaskSerializer(task)
            
            return Response(
                APIResponse.success(
                    data=response_serializer.data,
                    message="Task created successfully"
                ),
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                APIResponse.error(str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )


class TaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Get task details"""
        try:
            task = TaskService.get_task_report(request.user, pk)
            serializer = TaskSerializer(task)
            
            return Response(APIResponse.success(data=serializer.data))
        except Exception as e:
            return Response(
                APIResponse.error(str(e)),
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        """Update task status and completion details"""
        try:
            serializer = TaskUpdateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    APIResponse.error("Invalid data", serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            task = TaskService.update_task(request.user, pk, serializer.validated_data)
            response_serializer = TaskSerializer(task)
            
            return Response(
                APIResponse.success(
                    data=response_serializer.data,
                    message="Task updated successfully"
                )
            )
        except Exception as e:
            return Response(
                APIResponse.error(str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk):
        """Delete a task (Admin/SuperAdmin only)"""
        try:
            TaskService.delete_task(request.user, pk)
            return Response(
                APIResponse.success(message="Task deleted successfully"),
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                APIResponse.error(str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )


class TaskReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Get detailed task completion report"""
        try:
            task = TaskService.get_task_report(request.user, pk)
            
            if task.status != 'COMPLETED':
                return Response(
                    APIResponse.error("Task is not completed yet"),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer = TaskReportSerializer(task)
            return Response(APIResponse.success(data=serializer.data))
        except Exception as e:
            return Response(
                APIResponse.error(str(e)),
                status=status.HTTP_404_NOT_FOUND
            )


class TaskStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get task statistics for dashboard"""
        try:
            stats = TaskService.get_dashboard_stats(request.user)
            return Response(APIResponse.success(data=stats))
        except Exception as e:
            return Response(
                APIResponse.error(str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )