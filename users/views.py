from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.permissions import IsUser
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели User.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        """
        Проверяет права и исходя из этого разрешает / запрещает доступ эндпоинтам.
        """
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsUser]
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
