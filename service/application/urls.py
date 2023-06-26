from django.urls import include, path

app_name = 'application'

urlpatterns = [
    path(
        route='v1/',
        view=include('application.v1.urls', namespace='api_v1')
    )
]
