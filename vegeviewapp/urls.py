from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="HomePage"),
    path('home', views.index, name="HomePage"),
    path('signup', views.signup, name="Signup"),
    path('login', views.login, name="Login"),
    path('forgotpassword', views.forgotpassword, name="Forgot_Password"),
]