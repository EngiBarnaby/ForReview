from rest_framework.routers import DefaultRouter
from .views.main_views import Authorization
from .views.admin_views import UserAdminViewSet

r = DefaultRouter()
# пользовательское приложение
r.register('authorization', Authorization)

# админка
r.register('users', UserAdminViewSet)

urlpatterns = r.urls
