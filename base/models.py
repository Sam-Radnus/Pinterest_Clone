from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username = models.CharField(db_index=True, unique=True, max_length=255,null=True)
    email=models.EmailField(unique=True,null=True)
    password=models.CharField(unique=True, null=True,max_length=255)
    image=models.ImageField(null=True,upload_to="images/")
   
    USERNAME_FIELD ='email'

    
    REQUIRED_FIELDS = ['username']
    
    def total_followers(self):
        return self.followers

    def total_following(self):
        return self.following.count()    

class Post(models.Model):
    name=models.CharField(db_index=True,unique=False,max_length=255,null=True)  
    image=models.ImageField(null=True)
    caption=models.CharField(blank=True,max_length=255,null=True)
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    likes=models.ManyToManyField(User,related_name='likes',blank=True)
    time_created=models.DateTimeField(auto_now_add=True,null=True)
    tags=models.ManyToManyField('Tag',related_name='posts')
    def __str__(self):
        return self.name
    
    def LikedByUsers(self):
        return self.likes.all()
    def total_Likes(self):
        return self.likes.count()

class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='like_user')
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='like_post')
    created=models.DateTimeField(auto_now_add=True)     

    def __str__(self):
        return self.user.username

class UserFollowing(models.Model):
    user_id=models.ForeignKey("User",related_name="following",on_delete=models.CASCADE)
    following_user_id=models.ForeignKey("User",related_name="followers",on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together=('user_id','following_user_id')

    def __str__(self):
        return f"{self.user_id} follows {self.following_user_id}"    
    
    def getFollowers(self):
        return f"{self.user_id}"
    
class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    time_created=models.DateTimeField(auto_now_add=True)
    text=models.TextField(max_length=225)    

    def __str__(self):
        return self.text[0:50]
    
class Tag(models.Model):
    name=models.CharField(max_length=35)
    slug=models.CharField(max_length=250)
    created_at=models.DateTimeField(auto_now_add=False)


    def __str__(self):
        return self.name    