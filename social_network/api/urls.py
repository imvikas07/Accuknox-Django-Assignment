from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, UserSearchView, FriendRequestViewSet, FriendsListView, PendingRequestsView

router = DefaultRouter()
router.register(r'friend-requests', FriendRequestViewSet, basename='friend-request')

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friends/', FriendsListView.as_view(), name='friends-list'),
    path('pending-requests/', PendingRequestsView.as_view(), name='pending-requests'),
] + router.urls

