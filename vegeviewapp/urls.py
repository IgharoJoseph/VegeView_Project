from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="HomePage"),
    path('home', views.index, name="HomePage"),
    path('register', views.signup, name="SignUp"),
    path('login', views.user_login, name="Login"),
    path('logout', views.user_logout, name="Logout"),
    path('forgotpassword', views.forgotpassword, name="Forgot_Password"),
    path('data-access-viewer', views.data_access_viewer, name="Data-Access-Viewer")
]