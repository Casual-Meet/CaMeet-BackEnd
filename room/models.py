from django.db import models
from accounts.models import User


# Create your models here.
class Room(models.Model):
    user_key = models.ForeignKey(User, related_name='rooms',on_delete=models.CASCADE,null=True)
    # user_id = models.ManyToManyField(User, verbose_name='유저')
    room_title = models.CharField(max_length=20)
    room_interest = models.CharField(max_length=20)
    room_place =  models.CharField(max_length=50)
    room_date = models.DateField(null=False,blank=False)
    room_time = models.TimeField(null=False,blank=False)
    room_headcount = models.IntegerField(default=1)
    room_status = models.IntegerField(default=0)
    room_created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room_title}"

class Apply(models.Model):
    user_id = models.ForeignKey(User, related_name='join', on_delete=models.CASCADE)
    room_id = models.ForeignKey(Room, related_name='participant', on_delete=models.CASCADE)
    apply_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['apply_time']

    def __str__(self):
        return f"# {self.room_id.room_interest} : {self.room_id.room_title} / 참여자 : {self.user_id.email}"
