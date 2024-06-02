from django.shortcuts import render

# Create your views here.

from rest_framework import generics, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, FriendRequest
from .serializers import UserSerializer, RegisterSerializer, FriendRequestSerializer
from .throttles import FriendRequestThrottle
from django.db.models import Q

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email__iexact=email).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=400)

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        if '@' in query:
            return User.objects.filter(email__iexact=query)
        return User.objects.filter(name__icontains=query)

class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [FriendRequestThrottle]

    def get_queryset(self):
        return self.queryset.filter(Q(from_user=self.request.user) | Q(to_user=self.request.user))

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)

class FriendsListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        friends = User.objects.filter(
            Q(id__in=FriendRequest.objects.filter(
                to_user=request.user, status='accepted'
            ).values_list('from_user', flat=True)) |
            Q(id__in=FriendRequest.objects.filter(
                from_user=request.user, status='accepted'
            ).values_list('to_user', flat=True))
        )
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data)

class PendingRequestsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        pending_requests = FriendRequest.objects.filter(
            to_user=request.user, status='pending'
        )
        serializer = FriendRequestSerializer(pending_requests, many=True)
        return Response(serializer.data)
