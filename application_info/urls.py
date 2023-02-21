from rest_framework.routers import DefaultRouter

from .views.main_views import PostTopicsViewSet
from .views.main_views import PostViewSet
from .views.main_views import ReviewViewSet

from .views.admin_views import PostTopicAdminViewSet
from .views.admin_views import PostAdminViewSet
from .views.admin_views import PostImgAdminViewSet
from .views.admin_views import ReviewAdminViewSet
from .views.admin_views import ReviewImgAdminViewSet
from .views.admin_views import SystemConfigAdminViewSet
from .views.admin_views import LogAdminViewSet

from .views.statistic_views import ApplicationStatistic

r = DefaultRouter()

# пользовательское приложение
r.register('post_topics', PostTopicsViewSet)
r.register('posts', PostViewSet)
r.register('reviews', ReviewViewSet)

# админка
r.register('post_topics', PostTopicAdminViewSet)
r.register('posts', PostAdminViewSet)
r.register('posts_img', PostImgAdminViewSet)
r.register('reviews', ReviewAdminViewSet)
r.register('reviews_img', ReviewImgAdminViewSet)
r.register('system_configs', SystemConfigAdminViewSet)
r.register('logs', LogAdminViewSet)

# статистика
r.register('application_statistic', ApplicationStatistic)

urlpatterns = r.urls
