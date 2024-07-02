from django.db import models
from django.contrib.auth.models import User


class FriendRequest(models.Model):
        request_status=(
                ( 'pending','pending' ),
                ('accepted','accepted'),
                ('rejected','rejected')
        )
        sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
        receiver = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='received_requests')
        status = models.CharField(max_length=20,choices=request_status,default='pending')  # You can use choices for 'status' like 'pending', 'accepted', 'rejected'
        created_at = models.DateTimeField(auto_now_add=True)
        

        def __str__(self):
                return f"{self.sender} to {self.receiver} ({self.status})"

