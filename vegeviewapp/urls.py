from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="HomePage"),
    path('home', views.index, name="HomePage"),
    path('register', views.signup, name="SignUp"),
    path('login', views.user_login, name="Login"),
    path('forgotpassword', views.forgotpassword, name="Forgot_Password"),
]