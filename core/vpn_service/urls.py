from django.urls import path, re_path
from django.views.generic import RedirectView

from . import views

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    path('', views.main, name="main"),
    path('personal_cabinet/', views.personal_cabinet, name="personal_cabinet"),
    path('change_profile/', views.change_profile, name="change_profile"),
    path('create_site/', views.create_site, name="create_site"),
    path('<int:site_pk>/<slug:site_slug>/', views.site_view, name="site_origin"),
    path('<int:site_pk>/<slug:site_slug>/<path:domain_url>', views.site_view, name="site"),
    path('register/', views.register_user, name="registration"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_view, name="logout"),

    re_path(r'^favicon\.ico$', favicon_view)
]