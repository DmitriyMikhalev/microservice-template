import logging

from core.utils import get_logger_extra
from django.urls import reverse_lazy
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)

from .models import Task
from .paginations import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import TaskSerializer

logger = logging.getLogger(__name__)


class TaskViewDetail(RetrieveAPIView, DestroyAPIView, UpdateAPIView):
    serializer_class = TaskSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Task.objects.all()

    def delete(self, request, *args, **kwargs):
        self._add_log_data(request=request, pk=kwargs['pk'])

        return super().delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self._add_log_data(request=request, pk=kwargs['pk'])

        return super().get(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        self._add_log_data(request=request, pk=kwargs['pk'])

        return super().patch(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self._add_log_data(request=request, pk=kwargs['pk'])

        return super().update(request, *args, **kwargs)

    def _add_log_data(self, request, pk):
        path: str = reverse_lazy(
            kwargs={'pk': pk},
            viewname='application:api_v1:task-detail'
        )
        kwargs: dict[str, str] = get_logger_extra(request=request)
        logger.debug(
            extra=kwargs,
            msg=f'request for {path} accepted successfully.'
        )


class TaskView(ListAPIView, CreateAPIView):
    # Despite the fact that the restriction of the rights "author or read" is
    # used, in the methods associated with requests, the content of which the
    # user of the request is not the author is forcibly excluded, so the
    # restrictions are expanded to "only the author has access".
    serializer_class = TaskSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user)

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self._add_log_data(request=request)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self._add_log_data(request=request)

        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def _add_log_data(self, request):
        path: str = reverse_lazy(viewname='application:api_v1:task-list')
        kwargs: dict[str, str] = get_logger_extra(request=request)
        logger.debug(
            extra=kwargs,
            msg=f'request for {path} accepted successfully.'
        )
