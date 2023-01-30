from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Post)
admin.site.register(models.Like)
admin.site.register(models.UserFollowing)
admin.site.register(models.Comment)