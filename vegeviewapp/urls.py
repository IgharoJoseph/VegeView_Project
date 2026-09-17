from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="HomePage"),
    path('home', views.index, name="HomePage"),
    path('directory/', views.directory, name="DiseaseDirectory"),
    path('directory/<int:pk>/', views.disease_detail, name="DiseaseDetail"),
    path('diagnose/', views.diagnose, name="SymptomChecker"),
    path('fields/', views.field_map_view, name="FieldMap"),
    path('signup', views.signup, name="Signup"),
    path('login', views.login, name="Login"),
    path('logout', views.logout_view, name="Logout"),
    path('forgotpassword', views.forgotpassword, name="Forgot_Password"),
]
