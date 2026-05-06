from django.urls import path
from .views import ImportUsersView, UserListView, UserDetailView, UserDeleteView

urlpatterns = [
    # Import users from external API
    path('import/', ImportUsersView.as_view(), name='import-users'),
    
    # User list and operations
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
]