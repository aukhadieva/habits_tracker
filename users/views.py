from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.permissions import IsUser
from users.serializers import UserSerializer, UserListSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели User.
    """
    queryset = User.objects.all()

    def get_permissions(self):
        """
        Проверяет права и исходя из этого разрешает / запрещает доступ эндпоинтам
        и определяет сериализатор.
        """
        if self.action == "create":
            self.permission_classes = [AllowAny]
            self.serializer_class = UserSerializer
        if self.action in ["list"]:
            self.permission_classes = [IsAuthenticated]
            self.serializer_class = UserListSerializer
        if self.action in ["retrieve"]:
            self.permission_classes = [IsAuthenticated, IsUser]
            self.serializer_class = UserSerializer
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsUser]
            self.serializer_class = UserSerializer
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Хэширует создаваемый при регистрации пароль.
        """
        instance = serializer.save(is_active=True)
        instance.set_password(instance.password)
        instance.save()

    def perform_update(self, serializer):
        """
        Хэширует редактируемый пароль.
        """
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()
