from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .views import (RegisterView, ChangePasswordView, UpdateProfileView, 
                    LogoutView, LogoutAllView , PendingRequestListView, SendFriendRequestToUserView, 
                    AcceptRejectFriendRequestView , UserDetailView , UserListCreateView , FriendsListView)


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('friend-requests/', PendingRequestListView.as_view(), name='friend-requests'),
    path('get-friends/', FriendsListView.as_view(),name='get-friends'),
    path('accept-reject-friend-request/', AcceptRejectFriendRequestView.as_view(), name='accept-reject-friend-request'),
    path('send-friend-request-to-user/', SendFriendRequestToUserView.as_view(), name='send-friend-request-to-user'),    
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('update_profile/<int:pk>/', UpdateProfileView.as_view(), name='auth_update_profile'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('logout_all/', LogoutAllView.as_view(), name='auth_logout_all'),
]

