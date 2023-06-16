from django.urls import include, path
from .views import TaskView, TaskViewDetail


urlpatterns = [
    path(route='auth/', view=include('djoser.urls')),
    path(route='auth/', view=include('djoser.urls.jwt')),
    path(route='tasks/', view=TaskView.as_view(), name='task-list'),
    path(route='tasks/<int:pk>/', view=TaskViewDetail.as_view(),
         name='task-detail')
]
