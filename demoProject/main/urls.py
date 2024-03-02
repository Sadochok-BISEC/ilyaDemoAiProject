from django.urls import path
from . import views

urlpatterns = [
   path('home/', views.home, name='home'),
   path('empty_home/', views.logout_view, name="empty_home"),
   path('', views.logout_view, name="empty_home"),
   path('about', views.about, name='about'),
   path('contacts', views.contacts, name='contacts'),

   path('empty_home/sign-up', views.SignUpView.as_view(), name="signup"),
   path('empty_home/log-in', views.login_view, name="login"),
]