from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('dj_rest_auth.urls')),
    path('user/', include('dj_rest_auth.registration.urls')),
    path('user/', include('allauth.urls')),
    path('user/', include('user.urls')),
    path('room/', include('room.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
