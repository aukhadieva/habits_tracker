from rest_framework import viewsets

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели User.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

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
