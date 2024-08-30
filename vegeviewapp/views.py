from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'vegeviewapp/index.html')

def signup(request):
    return render(request, 'vegeviewapp/signup.html')

def login(request):
    return render(request, 'vegeviewapp/login.html')

def forgotpassword(request):
    return render(request, 'vegeviewapp/forgotpassword.html')
