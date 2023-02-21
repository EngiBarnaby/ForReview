from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from accounts.models import User
from accounts.serializers.admin_serializers import UserAdminSerializer


class UserAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    permission_classes = (IsAdminUser,)
    filterset_fields = ('email', 'name', 'is_active', 'is_staff', 'is_superuser',)
    search_fields = ('username', 'email', 'name',)
    ordering_fields = (
        'username', 'email', 'name', 'is_active', 'is_staff', 'is_superuser', 'date_joined',
        'rows_to_recalculate_available',
    )
