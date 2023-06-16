from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import Task


class TaskSerializer(ModelSerializer):
    author = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
