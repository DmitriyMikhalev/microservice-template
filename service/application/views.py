from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT,
                                   HTTP_206_PARTIAL_CONTENT,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .models import Task
from .permissions import IsAuthorOrReadOnly
from .serializers import TaskSerializer


class TaskView(APIView, PageNumberPagination):
    page_size = 3
    permission_classes = (IsAuthorOrReadOnly,)

    def get(self, request):
        queryset = Task.objects.filter(author=request.user)  # hide other
        tasks = self.paginate_queryset(
            queryset=queryset,
            request=request,
            view=self
        )
        serializer = TaskSerializer(instance=tasks, many=True)

        return self.get_paginated_response(data=serializer.data)

    def post(self, request):
        is_many = isinstance(request.data, list)
        serializer = TaskSerializer(data=request.data, many=is_many)

        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(data=serializer.data, status=HTTP_200_OK)

        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


class TaskViewDetail(APIView):
    permission_classes = (IsAuthorOrReadOnly,)

    def delete(self, request, pk):
        task = get_object_or_404(klass=Task, pk=pk)
        self.check_object_permissions(request, task)

        task.delete()

        return Response(status=HTTP_204_NO_CONTENT)

    def get(self, request, pk):
        task = get_object_or_404(klass=Task, pk=pk)
        self.check_object_permissions(request, task)

        serializer = TaskSerializer(instance=task)
        return Response(data=serializer.data, status=HTTP_200_OK)

    def patch(self, request, pk):
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

    def post(self, request, pk):
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(data=serializer.data, status=HTTP_201_CREATED)

        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        task = get_object_or_404(klass=Task, pk=pk)
        self.check_object_permissions(request, task)

        serializer = TaskSerializer(data=request.data, instance=task)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=HTTP_200_OK)

        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)
