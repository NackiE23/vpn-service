from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name="main"),
    path('personal_cabinet/', views.personal_cabinet, name="personal_cabinet"),
    path('register/', views.register_user, name="registration"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_view, name="logout"),
]