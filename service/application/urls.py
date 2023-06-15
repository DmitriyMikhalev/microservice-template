from django.urls import include, path

urlpatterns = [
    path(route='auth/', view=include('djoser.urls')),
    path(route='auth/', view=include('djoser.urls.jwt'))
]