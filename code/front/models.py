from __future__ import unicode_literals
from django.db import models

class WebUser(models.Model):
    user_id=models.AutoField(primary_key=True)
    user_name=models.CharField(max_length=30)
    user_password=models.CharField(max_length=30)


class Video(models.Model):
    video_id=models.AutoField(primary_key=True)
    video_name=models.CharField(max_length=30)
    video_address=models.CharField(max_length=30)
    user_id=models.ForeignKey(to="WebUser",on_delete=models.CASCADE)

class Comment(models.Model):
    comment_id=models.AutoField(primary_key=True)
    comment_word=models.CharField(max_length=30)
    user_id=models.ForeignKey(to="WebUser",on_delete=models.CASCADE)
    video_id=models.ForeignKey(to="Video",on_delete=models.CASCADE)

class Share(models.Model):
    share_id=models.AutoField(primary_key=True)
    user1_id=models.ForeignKey(to="WebUser",on_delete=models.CASCADE,related_name='user1')
    user2_id=models.ForeignKey(to="WebUser",on_delete=models.CASCADE,related_name='user2')
    video_id=models.ForeignKey(to="Video",on_delete=models.CASCADE)