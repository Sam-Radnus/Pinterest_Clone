from django.contrib import admin
from django.urls import path,include,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path('',views.home,name='landing'),
    path('loginPage',views.loginPage,name='login'),
    path('upload',views.upload,name='upload'),
    path('dashboard',views.dashboard,name='profile'),
    path('register',views.register,name='register'),
    path('logout',views.logoutUser,name='logout'),
    path('updateProfile/',views.updateUser,name='update-user'),
    path('post/<str:pk>',views.userPost,name='view-post'),
    path('post/like/<str:pk>',views.toggleLike,name='like-post'),
    path('user/profile/<str:pk>',views.userProfile,name='user-profile'),
    path('user/follow/<str:pk>/<str:action>',views.addFollower,name='follow-user'),
    path('post/<str:pk>/<str:sk>',views.createComment,name='add-comment')
]
