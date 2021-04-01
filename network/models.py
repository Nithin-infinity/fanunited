from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone



class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(default='images/profile_pic/default.jpg', upload_to='images/profile_pic/')
    title = models.CharField(max_length=250, blank=True, null=True)
    about = models.CharField(max_length=500, blank=True, null=True)
    dob = models.DateField(blank =True, null=True)
    following = models.ManyToManyField(User, related_name='followers', blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Post(models.Model):
    content = models.CharField(max_length=500)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'posts')
    likedUsers = models.ManyToManyField(User, related_name='likedPosts', blank=True)

    def __str__(self):
        return f"Post: Created by {self.creator}"
    
    @property
    def isUpdated(self):
        return False if self.dateCreated.minute == self.dateUpdated.minute else True

    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=500)
    commenter = models.ForeignKey(User, on_delete = models.CASCADE, related_name='comments')
    created = models.DateField(auto_now_add = True)
    modfified = models.DateField(auto_now = True)
    likedUsers = models.ManyToManyField(User, related_name='likedComments', blank=True)

    def __str__(self):
        return f"comment: {self.id}"

