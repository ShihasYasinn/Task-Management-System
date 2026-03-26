from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator

from users.services.user_service import UserService
from users.serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer, ChangePasswordSerializer
)
from commons.utils.response import APIResponse


class UserListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get users with filtering and pagination"""
        try:
            # Get filter parameters
            filters = {
                'role': request.GET.get('role'),
                'is_active': request.GET.get('is_active'),
                'search': request.GET.get('search'),
            }
            
            # Convert is_active to boolean
            if filters['is_active'] is not None:
                filters['is_active'] = filters['is_active'].lower() == 'true'
            
            # Remove None values
            filters = {k: v for k, v in filters.items() if v is not None and v != ''}
            
            users = UserService.get_users(request.user, filters)
            
            # Pagination
            page = request.GET.get('page', 1)
            page_size = request.GET.get('page_size', 20)
            
            paginator = Paginator(users, page_size)
            page_obj = paginator.get_page(page)
            
            serializer = UserSerializer(page_obj.object_list, many=True)
            
            return Response(APIResponse.success(data={
                'users': serializer.data,
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
        """Create a new user (Admin/SuperAdmin only)"""
        try:
            serializer = UserCreateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    APIResponse.error("Invalid data", serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Process data through service
            validated_data = UserService.create_user(request.user, serializer.validated_data)
            user = serializer.create(validated_data)
            
            response_serializer = UserSerializer(user)
            
            return Response(
                APIResponse.success(
                    data=response_serializer.data,
                    message="User created successfully"
                ),
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                APIResponse.error(str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )


class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Get user details"""
        try:
            users = UserService.get_users(request.user)
            user = users.get(id=pk)
            serializer = UserSerializer(user)
            
            return Response(APIResponse.success(data=serializer.data))
        except Exception as e:
            return Response(
                APIResponse.error(str(e)),
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        """Update user information"""
        try:
            serializer = UserUpdateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    APIResponse.error("Invalid data", serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user = UserService.update_user(request.user, pk, serializer.validated_data)
            response_serializer = UserSerializer(user)
            
            return Response(
                APIResponse.success(
                    data=response_serializer.data,
                    message="User updated successfully"
                )
            )
        except Exception as e:
            return Response(
                APIResponse.error(str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk):
        """Delete a user (SuperAdmin only)"""
        try:
            UserService.delete_user(request.user, pk)
            return Response(
                APIResponse.success(message="User deleted successfully"),
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                APIResponse.error(str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Change user password"""
        try:
            serializer = ChangePasswordSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    APIResponse.error("Invalid data", serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            UserService.change_password(
                request.user,
                serializer.validated_data['old_password'],
                serializer.validated_data['new_password']
            )
            
            return Response(
                APIResponse.success(message="Password changed successfully")
            )
        except Exception as e:
            return Response(
                APIResponse.error(str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )


class UserStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get user statistics"""
        try:
            stats = UserService.get_user_stats(request.user)
            return Response(APIResponse.success(data=stats))
        except Exception as e:
            return Response(
                APIResponse.error(str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )
