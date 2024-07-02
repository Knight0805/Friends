from functools import wraps

from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics , status
#from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny,  IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken,  OutstandingToken , BlacklistedToken
from rest_framework.response import Response
from rest_framework.views import APIView 

from .utils import MultiFieldSearchFilter , custom_ratelimiter
from .serializer import (RegisterSerializer 
                         , ChangePasswordSerializer, UpdateUserSerializer 
                        , FriendRequestSerializer , UserSerializer)
from .models import FriendRequest


# class UserListCreateView(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    
class RegisterView(generics.CreateAPIView):
        queryset = User.objects.all()
        permission_classes = (AllowAny,)
        serializer_class = RegisterSerializer


class UserListCreateView(generics.ListCreateAPIView):
    search_fields = ['first_name', "last_name", "email" ,'username']
    filter_backends = [MultiFieldSearchFilter]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class SendFriendRequestToUserView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]


    def create(self,request,*args, **kwargs):
        try:
            user = self.request.user
            if custom_ratelimiter(self.request) != True:
                return Response({'detail': "Rate limit exceeded"}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            
            recipient_id = request.data.get('recipient_id')
            serializer = self.get_serializer(data=request.data)
            recipient_user = User.objects.get(pk=int(recipient_id))
            
            if (check_request := FriendRequest.objects.filter(sender=user, receiver=recipient_user)):
                return Response({'detail': 'Request already send!'}, status=status.HTTP_400_BAD_REQUEST)
            
            
            
            if not recipient_id :
                return Response({'detail': 'Request does not conatins Recipient ID.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Try to get the recipient user
            if user.id != recipient_id:
                recipient_user = User.objects.get(pk=int(recipient_id))
                serializer.is_valid(raise_exception=True)
                serializer.save(sender=user,receiver=recipient_user)
                return Response({'detail': 'We have sent your request'}, status=status.HTTP_201_CREATED)
            
            return Response({'detail': 'Invaild ID'}, status=status.HTTP_400_BAD_REQUEST)
        
        except User.DoesNotExist:
            return Response({'detail': 'Recipient user does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        # Validate and save the serializer
        
        
        
class PendingRequestListView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(receiver=user,status='pending')


class FriendsListView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(Q(sender=user) | Q(receiver=user) & Q(status='accepted'))
    
    
class AcceptRejectFriendRequestView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request):
        instance = FriendRequest.objects.get(pk=request.data.get('request_id'))
        if self.request.user.id != instance.receiver.pk:
            return  Response({'detail': f'Invaild Request! Only recever can accpet the request!'}, status=status.HTTP_400_BAD_REQUEST)
        
        request_status =request.data.get('status')
        
        if instance.status != 'pending':
            return Response({'detail': f'Invaild Request ! Its already done ! {request_status}'}, status=status.HTTP_400_BAD_REQUEST)
        
        instance.status = request_status
        instance.save()
        notification_message = f"Your friend request to {instance.sender} has been {request_status}."
        return Response({'detail': notification_message}, status=status.HTTP_200_OK)



class ChangePasswordView(generics.UpdateAPIView):
        queryset = User.objects.all()
        permission_classes = (IsAuthenticated,)
        serializer_class = ChangePasswordSerializer


class UpdateProfileView(generics.UpdateAPIView):
        queryset = User.objects.all()
        permission_classes = (IsAuthenticated,)
        serializer_class = UpdateUserSerializer


class LogoutView(APIView):
        permission_classes = (IsAuthenticated,)

        def post(self, request):
            try:
                refresh_token = request.data["refresh_token"]
                token = RefreshToken(refresh_token)
                token.blacklist()

                return Response(status=status.HTTP_205_RESET_CONTENT)
            except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(APIView):
        permission_classes = (IsAuthenticated,)

        def post(self, request):
            tokens = OutstandingToken.objects.filter(user_id=request.user.id)
            for token in tokens:
                t, _ = BlacklistedToken.objects.get_or_create(token=token)

            return Response(status=status.HTTP_205_RESET_CONTENT)

