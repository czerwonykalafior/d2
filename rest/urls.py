from django.conf.urls import url
from django.urls import include

from rest_framework import routers

from rest.views import UserViewSet, get_data, some_streaming_csv_view

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'get_data', get_data, name='get_data'),
    url(r'download', some_streaming_csv_view, name='download'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
