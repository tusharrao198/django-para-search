from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'password', 'email', 'is_staff']

    def create(self,validated_data):
        user = User.objects.create_user(username=validated_data['username'], email=validated_data['email'] , is_staff=validated_data['is_staff'])
        user.set_password(validated_data['password'])
        user.save()
        return user


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += [
    path('admin/', admin.site.urls),
    
    path('', include('cuboidapp.urls')),        
    path('api-token-auth/', views.obtain_auth_token),    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

