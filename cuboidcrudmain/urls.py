from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('cuboidapp.urls')),
    
    path('auth/', include('rest_authtoken.urls')),
    
    path('api-token-auth/', views.obtain_auth_token),

    # path('rest-auth/', include('rest_auth.urls')),    
    # path('rest-auth/registration/', include('rest_auth.registration.urls')),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
