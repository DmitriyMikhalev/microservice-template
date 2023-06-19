import logging

from core.utils import get_logger_extra
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT,
                                   HTTP_206_PARTIAL_CONTENT,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView

from .models import Task
from .permissions import IsAuthorOrReadOnly
from .serializers import TaskSerializer
from django.urls import reverse_lazy

logger = logging.getLogger(__name__)


class TaskView(APIView, PageNumberPagination):
    """
    Despite the fact that the restriction of the rights "author or read" is
    used, in the methods associated with requests, the content of which the
    user of the request is not the author is forcibly excluded, so the
    restrictions are expanded to "only the author has access".
    """
    page_size = 3

    def get(self, request):
        self._add_log_data(request=request)

        queryset = Task.objects.filter(author=request.user)  # hide other
        tasks = self.paginate_queryset(
            queryset=queryset,
            request=request,
            view=self
        )
        serializer = TaskSerializer(instance=tasks, many=True)

        return self.get_paginated_response(data=serializer.data)

    def post(self, request):
        self._add_log_data(request=request)

        is_many: bool = isinstance(request.data, list)
        serializer = TaskSerializer(data=request.data, many=is_many)

        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(data=serializer.data, status=HTTP_201_CREATED)

        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

    def _add_log_data(self, request):
        path: str = reverse_lazy(viewname='application:api_v1:task-list')
        kwargs: dict[str, str] = get_logger_extra(request=request)
        logger.debug(
            extra=kwargs,
            msg=f'request for {path} accepted successfully.'
        )


class TaskViewDetail(APIView):
    permission_classes = (IsAuthorOrReadOnly,)

    def delete(self, request, pk):
        self._add_log_data(request=request, pk=pk)

        task = get_object_or_404(klass=Task, pk=pk)
        self.check_object_permissions(request, task)

        task.delete()

        return Response(status=HTTP_204_NO_CONTENT)

    def get(self, request, pk):
        self._add_log_data(request=request, pk=pk)

        task = get_object_or_404(klass=Task, pk=pk)
        self.check_object_permissions(request, task)

        serializer = TaskSerializer(instance=task)
        return Response(data=serializer.data, status=HTTP_200_OK)

    def patch(self, request, pk):
        self._add_log_data(request=request, pk=pk)

        task = get_object_or_404(klass=Task, pk=pk)
        self.check_object_permissions(request, task)

        serializer = TaskSerializer(
            data=request.data,
            instance=task,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=HTTP_206_PARTIAL_CONTENT
            )

        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        self._add_log_data(request=request, pk=pk)

        task = get_object_or_404(klass=Task, pk=pk)
        self.check_object_permissions(request, task)

        serializer = TaskSerializer(data=request.data, instance=task)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=HTTP_200_OK)

        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

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
