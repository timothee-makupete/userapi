from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from .models import User
from .serializers import UserSerializer
from .utils import fetch_external_users, transform_user_data

@extend_schema_view(
    post=extend_schema(
        tags=['Import'],
        summary="Import users from external API",
        description="Fetches user data from JSONPlaceholder API and stores it in the database. Handles API unavailability gracefully.",
        responses={
            200: OpenApiTypes.OBJECT,
            401: OpenApiTypes.OBJECT,
            503: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                'Success Response',
                value={
                    "status": "success",
                    "message": "Import completed",
                    "created": 10,
                    "updated": 0,
                    "total_processed": 10,
                    "errors": None
                },
                response_only=True
            ),
            OpenApiExample(
                'API Unavailable',
                value={
                    "error": "API connection failed: Unable to reach the server",
                    "status": "failed"
                },
                response_only=True
            ),
        ]
    )
)
class ImportUsersView(APIView):
    """Endpoint to trigger import of users from external API"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        success, data = fetch_external_users()
        
        if not success:
            return Response(
                {'error': data, 'status': 'failed'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        created_count = 0
        updated_count = 0
        errors = []
        
        for ext_user in data:
            try:
                user_data = transform_user_data(ext_user)
                address_data = user_data.pop('address')
                company_data = user_data.pop('company')
                
                from .models import Address, Company
                address, _ = Address.objects.get_or_create(**address_data)
                company, _ = Company.objects.get_or_create(
                    name=company_data['name'],
                    defaults={
                        'catch_phrase': company_data.get('catch_phrase', ''),
                        'bs': company_data.get('bs', '')
                    }
                )
                
                obj, created = User.objects.update_or_create(
                    external_id=user_data['external_id'],
                    defaults={
                        **user_data,
                        'address': address,
                        'company': company
                    }
                )
                
                if created:
                    created_count += 1
                else:
                    updated_count += 1
                    
            except Exception as e:
                errors.append(f"User ID {ext_user.get('id')}: {str(e)}")
        
        return Response({
            'status': 'success',
            'message': 'Import completed',
            'created': created_count,
            'updated': updated_count,
            'total_processed': created_count + updated_count,
            'errors': errors if errors else None
        }, status=status.HTTP_200_OK)


@extend_schema_view(
    get=extend_schema(
        tags=['Users', 'Filters'],
        summary="List all users with optional filtering",
        description="Returns a list of all users. Can be filtered by city, company name, or user name. Supports combining multiple filters.",
        parameters=[
            OpenApiParameter(
                name='city',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description='Filter by city (case-insensitive, partial match)',
                examples=[OpenApiExample('Example', value='Gwenborough')]
            ),
            OpenApiParameter(
                name='company',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description='Filter by company name (case-insensitive, partial match)',
                examples=[OpenApiExample('Example', value='Romaguera')]
            ),
            OpenApiParameter(
                name='name',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description='Filter by user name (case-insensitive, partial match)',
                examples=[OpenApiExample('Example', value='Leanne')]
            ),
        ],
        responses={200: UserSerializer(many=True)}
    )
)
class UserListView(generics.ListAPIView):
    """List all users with filtering support (city, company, name)"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    
    def get_queryset(self):
        queryset = User.objects.select_related('address', 'company').all()
        
        city = self.request.query_params.get('city')
        if city:
            queryset = queryset.filter(address__city__icontains=city)
        
        company = self.request.query_params.get('company')
        if company:
            queryset = queryset.filter(company__name__icontains=company)
        
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        
        return queryset


@extend_schema_view(
    get=extend_schema(
        tags=['Users'],
        summary="Get a single user by ID",
        description="Returns detailed information about a specific user including their address and company.",
        responses={
            200: UserSerializer,
            401: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        }
    )
)
class UserDetailView(generics.RetrieveAPIView):
    """Get a single user by ID"""
    queryset = User.objects.select_related('address', 'company').all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


@extend_schema_view(
    delete=extend_schema(
        tags=['Users'],
        summary="Delete a user by ID",
        description="Permanently removes a user from the database. The address and company records remain if shared with other users.",
        responses={
            200: OpenApiTypes.OBJECT,
            401: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                'Success Response',
                value={
                    "message": "User \"Leanne Graham\" (ID: 1) has been deleted successfully"
                },
                response_only=True
            )
        ]
    )
)
class UserDeleteView(generics.DestroyAPIView):
    """Delete a user by ID"""
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user_id = instance.id
        user_name = instance.name
        instance.delete()
        
        return Response({
            'message': f'User "{user_name}" (ID: {user_id}) has been deleted successfully'
        }, status=status.HTTP_200_OK)