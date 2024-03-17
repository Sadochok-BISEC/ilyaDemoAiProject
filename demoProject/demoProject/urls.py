# Root demoProject urls

#from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('demoProject/', include('main.urls')),
    path('', include('main.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    #path('api/', include('main.urls')),
    #path("", include("main.urls", namespace="main")),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
