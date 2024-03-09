from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import UserSignUpForm, UserLoginForm, UserEditForm, userProfileEditForm
from .models import UserProfile
# Create your views here.
def userLogin(request):
    page = 'login'
    form = UserLoginForm()
    if request.method == "POST":
        # username = request.POST.get("username")
        # password = request.POST.get("password")
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:    
                user =User.objects.get(username=username)
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("/server/dashboard")
            except:
                form["username"].field.widget.attrs['class'] += ' is-invalid'
                form["password"].field.widget.attrs['class'] += ' is-invalid'
                messages.error(request, "Invalid username or password")
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
            
    context = {'page':page,"form":form}
    return render(request, "Auth/Authentication.html", context)

def userLogout(request):
    logout(request)
    return redirect("/")

def userRegistration(request):
    form = UserSignUpForm()
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1'),
                email=form.cleaned_data.get('email')
            )
            user_profile = UserProfile(user=user)
            # user = form.save(commit=False)
            # user.username = form.cleaned_data.get('username')
            user_profile.save()
            login(request, user)
            return redirect('/server/dashboard')
        else:
            print(form.errors)
            for field in form.errors:
                print(field)
                form[field].field.widget.attrs['class'] += ' is-invalid'
            # for error in form.errors:
            #     messages.error(request, form.errors[error])
            #     return redirect(request.path)
            # return render(request, "Auth/Authentication.html", {"form":form})
            # messages.error(request, "Something went wrong. Please try again.")
    return render(request, "Auth/Authentication.html", {"form":form})

def getUsers(request):
    users = UserProfile.objects.all()
    print(users)

    context = {"users":users}
    return render(request, "Users/GetUsers.html", context)

def userEdit(request,id):
    user = UserProfile.objects.get(id=id)
    form = UserEditForm(instance=user)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/users/get_users')
        else:
            print(form.errors)
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
    else:
        form = UserEditForm(instance=user)
    context = {"form":form}
    return render(request, "Users/EditUser.html", context)

def userDelete(request,id):

    user = UserProfile.objects.get(id=id)
    if request.user.username == user.user.username:
        messages.error(request, "You cannot delete yourself")
    else:
        user.delete()
    return redirect('/users/get_users')

def userProfileEdit(request):
    user = User.objects.get(id = request.user.id)
    form = userProfileEditForm(instance=user)
    if request.method == 'POST':
        form = userProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/server/dashboard')
        else:
            print(form.errors)
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
    else:
        form = userProfileEditForm(instance=user)
    context = {"form":form}
    return render(request, "Users/EditProfile.html", context)
