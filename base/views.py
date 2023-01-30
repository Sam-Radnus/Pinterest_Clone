from django.http import JsonResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from .forms import MyUserCreationForm,UserForm2,PostForm,UpdateForm,TagForm
from django.contrib import messages
from django.forms import formset_factory
from .models import User,Post,UserFollowing,Comment
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
# Create your views here.
import math
def welcome(request):
    context={'user':''}
    if request.user.is_authenticated:
        user=request.user
        context={'user':user}
    return render(request,'base/index.html',context)

def loginPage(request):
    if request.method=='POST':
       email=request.POST.get('email')
       password=request.POST.get('password')
       print(email)
       print(password)
       try:
           user=User.objects.get(email=email)
       except:
           messages.error(request,'User Not Found')
       user=authenticate(request,email=email,password=password)        
       print(user)
       if user is not None:
           login(request,user)
           return redirect('landing')
    return render(request,'base/login.html')

def dashboard(request):
    if request.user.is_authenticated:
        user=request.user
        temp=User.objects.get(email=user.email)
        print(temp)
       
        context={'user':user}
        return render(request,'base/profile.html',context)
    else:
        return redirect(request,'landing')


def upload(request):
    TagsForm=formset_factory(TagForm)
    if request.method=='POST':  
        form=PostForm(request.POST,request.FILES)
        if form.is_valid():
           
           post=Post.objects.create(
                user=request.user,
                image=form.cleaned_data['image'],
                name=request.POST.get('name'),
                caption=request.POST.get('caption'),
            )
        print(request.POST.get('image'))
        return redirect('landing') 
    return render(request,'base/upload_section.html',{'form':PostForm,'f':TagsForm})

def register(request):
   
    form=MyUserCreationForm()
    if request.method=='POST':
       form=MyUserCreationForm(request.POST,request.FILES)
       print(form)
       
       for field in form:
            print("Field Error:", field.value,  field.errors)
       if form.is_valid():
          user=form.save(commit=False)
          
          saved_user=user.save()
          print(saved_user)
        
          email=form.cleaned_data['email']
          password=form.cleaned_data['password1']
          user = authenticate(request, email=email, password=password)
          login(request,user)
          return redirect('landing')
       else:
          print(form)
          messages.error(request,'error occurred')   

   
    return render(request,'base/signup.html',{'form':form})

def logoutUser(request):
    logout(request)
    return redirect('landing')

def home(request):
    posts=Post.objects.all().order_by('-id')
    # print(posts)
    # struct_posts=[]
    # index=1
    # for i in range(math.ceil(len(posts)/4)):
    #       struct_posts.append([])
    #       for n in range(4):
    #           print(struct_posts[i])
    #           try:
    #              struct_posts[i].append(posts.get(id=str(index)))
               
    #           except:
    #              print(None)  
    #           index=index+1

    return render(request,'base/landingV2.html',{'range':range(4),'posts':posts})

def updateUser(request):
    if request.user.is_anonymous==True:
       home(request)
    user=request.user
    print(request.user)
    form=UserForm2(instance=user)
    if request.method=='POST':
        form=UserForm2(request.POST,request.FILES,instance=user)
        print('received')
        print(form.is_valid())
  
        if form.is_valid():
            print('saved')
            form.save()
            return redirect('landing')
        else:
            print(form)
            for field in form:
                print("Field Error:", field.value,  field.errors)
            #print(form.errors.as_json())
            #print(form)
            messages.error(request,'error occurred')   
    return render(request,'base/update_user.html',{'form':form})    




def userPost(request,pk):
    post=Post.objects.get(id=pk)
    post_likes=get_object_or_404(Post,id=pk)
    total_Likes=post_likes.total_Likes()
    saved=(request.user in post_likes.LikedByUsers())
    
    print(request.user)
    print(post_likes.LikedByUsers())
    comments=Comment.objects.filter(post=post)
    return render(request,'base/post.html',{'post':post,'total_Likes':total_Likes,'comments':comments,'saved':saved})

def toggleLike(request,pk):
    print('Post Liked')
    post=get_object_or_404(Post,id=pk)
    print(post)
    print(post.likes)
    print(request.user)
    if post.likes.filter(id=request.user.id).exists():
       post.likes.remove(request.user)
      
       print('Liked')
    else:
       post.likes.add(request.user)
       print('UnLiked')
    return redirect('view-post',pk)      

def userProfile(request,pk):
    requested_user=User.objects.get(id=pk)
    print(requested_user)
    followers=(UserFollowing.objects.filter(following_user_id=requested_user))
    following=(UserFollowing.objects.filter(user_id=requested_user)).count()
    already_following=False
    for users in followers.values():
        print(users)
        if(users.get('user_id_id')==request.user.id):
           print('set')
           already_following=True
           break
        else:
            already_following=False
    posts=(Post.objects.filter(user=requested_user))
    post_count=posts.count
    return render(request,'base/profile.html',{'user':requested_user,'followers':followers.count(),'following':following,'posts':posts,'post_count':post_count,'already_following':already_following})

def addFollower(request,pk,action):
    user_tf=User.objects.get(id=pk)
    currentUser=User.objects.get(id=request.user.id)
    print(action)
    if user_tf.id != currentUser.id:
       if action=='follow':
          requested_user=User.objects.get(id=pk)
          followers=(UserFollowing.objects.filter(following_user_id=user_tf)).count()
          try: 
             UserFollowing.objects.create(user_id=currentUser,following_user_id=user_tf)       
          except:
             pass
       if action=='unfollow':
           followers=(UserFollowing.objects.filter(following_user_id=user_tf))
           for users in followers.values():
              if(users.get('user_id_id')==request.user.id):
                  print('set')
                  UserFollowing.objects.filter(user_id_id=request.user.id).delete()
                  break
              else:
                  print('error removing')
          
       #return redirect(request,'user-profile ',{'user':requested_user,'followers':followers})

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def createComment(request,pk,sk):
    user=User.objects.get(id=pk)
    post=Post.objects.get(id=sk)
    text=request.POST.get('body')
    print(request.user)
    print(text)
    if text=='' or request.user.is_anonymous == True:
        print('test case')
        messages.info(request, 'Your password has been changed successfully!')
        pass
    else:
        comment=Comment.objects.create(
            user=request.user,
            post=post,
            text=request.POST.get('body')
        
        )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



