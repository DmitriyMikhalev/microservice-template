from django.urls import path, include

app_name = 'application'

urlpatterns = [
    path('v1/', include('application.v1.urls', namespace='api_v1'))
]
