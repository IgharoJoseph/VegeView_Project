from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import UserSignupForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .serializers import UserSignupSerializer
from django.conf import settings
from django.contrib import messages


# Traditional view for rendering HTML templates
def index(request):
    return render(request, 'vegeviewapp/index.html')

def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            # Serialize the form data
            serializer = UserSignupSerializer(data=form.cleaned_data)
            if serializer.is_valid():
                # Create the user using the serializer
                user = serializer.save()
                # Authenticate and log in the user
                user = authenticate(username=user.username, password=form.cleaned_data['password'])
                if user is not None:
                    auth_login(request, user)
                    return redirect('Login')  # Redirect to the home page after signup and login
            else:
                # If serializer is invalid, add errors to the form
                form.add_error(None, serializer.errors)
    else:
        form = UserSignupForm()

    return render(request, 'vegeviewapp/register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            # Get cleaned data from the form
            username_or_email = form.cleaned_data.get('username_or_email')
            password = form.cleaned_data.get('password')

            # Handle email or username login
            try:
                if '@' in username_or_email:
                    # Try to authenticate by email
                    user = User.objects.get(email=username_or_email)
                else:
                    # Try to authenticate by username
                    user = User.objects.get(username=username_or_email)

                # Authenticate the user using the username
                authenticated_user = authenticate(username=user.username, password=password)

                if authenticated_user is not None:
                    # Log the user in
                    auth_login(request, authenticated_user)
                    return redirect('Data-Access-Viewer')  
                else:
                    # Invalid password
                    form.add_error(None, 'Invalid login credentials')
            except User.DoesNotExist:
                # Invalid email/username
                form.add_error(None, 'No user found with this email or username')
    else:
        form = UserLoginForm()

    return render(request, 'vegeviewapp/login.html', {'form': form})

def user_logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully')
    return render(request, 'vegeviewapp/index.html')
    

def forgotpassword(request):
    return render(request, 'vegeviewapp/forgotpassword.html')

@login_required(login_url='Login') 
def data_access_viewer(request):
    return render (request, 'vegeviewapp/data-access-viewer.html')