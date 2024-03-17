from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
   path('home/', views.home, name='home'),
   path('empty_home/', views.logout_view, name="empty_home"),
   path('', views.logout_view, name="empty_home"),
   path('about', views.about, name='about'),
   path('contacts', views.contacts, name='contacts'),

   #path('empty_home/sign-up', views.SignUpView.as_view(), name="signup"),
   #path('empty_home/log-in', views.login_view, name="login"),

   # token
   path("empty_home/signup", views.UserRegisterationAPIView.as_view(), name="signup"),
   path("empty_home/login", views.UserLoginAPIView.as_view(), name="login"),
   path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
   path("empty_home/", views.UserLogoutAPIView.as_view(), name="empty_home"),
   path("", views.UserAPIView.as_view(), name="user-info"),
]