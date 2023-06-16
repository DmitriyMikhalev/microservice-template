from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from application.serializers import TaskSerializer

User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta:
        fields = (
            'email',
            'first_name',
            'id',
            'last_name',
            'password',
            'username',
        )
        model = User


class UserSerializer(BaseUserSerializer):
    tasks = TaskSerializer(read_only=True, many=True)

    class Meta:
        fields = (
            'email',
            'first_name',
            'id',
            'last_name',
            'username',
            'tasks'
        )
        model = User
