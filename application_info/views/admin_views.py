from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser

from django_filters.rest_framework import DjangoFilterBackend

from application_info.models import PostTopic
from application_info.models import Post
from application_info.models import PostImg
from application_info.models import Review
from application_info.models import ReviewImg
from application_info.models import SystemConfig
from application_info.models import Log

from application_info.serializers.admin_serializers import PostTopicAdminSerializer
from application_info.serializers.admin_serializers import PostAdminSerializer
from application_info.serializers.admin_serializers import PostImgAdminSerializer
from application_info.serializers.admin_serializers import ReviewAdminSerializer
from application_info.serializers.admin_serializers import ReviewImgAdminSerializer
from application_info.serializers.admin_serializers import SystemConfigAdminSerializer
from application_info.serializers.admin_serializers import LogAdminSerializer


class PostTopicAdminViewSet(viewsets.ModelViewSet):
    queryset = PostTopic.objects.all()
    serializer_class = PostTopicAdminSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    permission_classes = (IsAdminUser,)
    filterset_fields = ('name',)
    search_fields = ('name',)
    ordering_fields = ('name',)


class PostAdminViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostAdminSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    permission_classes = (IsAdminUser,)
    filterset_fields = ('topic', 'name', 'is_faq', 'is_notify', 'is_news',)
    search_fields = ('topic__name', 'name', 'short_text', 'article',)
    ordering_fields = ('topic__name', 'name', 'short_text', 'publication_time', 'is_faq', 'is_notify', 'is_news')


class PostImgAdminViewSet(viewsets.ModelViewSet):
    queryset = PostImg.objects.all()
    serializer_class = PostImgAdminSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    permission_classes = (IsAdminUser,)
    filterset_fields = ('post',)
    search_fields = ('post__name',)
    ordering_fields = ('post__name',)


class ReviewAdminViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewAdminSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    permission_classes = (IsAdminUser,)
    filterset_fields = ('grade', 'user',)
    search_fields = ('user__name', 'user__email', 'text',)
    ordering_fields = ('grade', 'text', 'user__name', 'created',)


class ReviewImgAdminViewSet(viewsets.ModelViewSet):
    queryset = ReviewImg.objects.all()
    serializer_class = ReviewImgAdminSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    permission_classes = (IsAdminUser,)
    filterset_fields = ('review',)
    search_fields = ('review__text',)
    ordering_fields = ('review__text',)


class SystemConfigAdminViewSet(viewsets.ModelViewSet):
    queryset = SystemConfig.objects.all()
    serializer_class = SystemConfigAdminSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    permission_classes = (IsAdminUser,)
    filterset_fields = ('is_actual', 'version_suffix',)
    search_fields = ('name', 'description', 'version', 'version_suffix',)
    ordering_fields = ('name', 'description', 'version', 'version_suffix', 'is_actual', 'start_date',)


class LogAdminViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogAdminSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    permission_classes = (IsAdminUser,)
    filterset_fields = (
        'section', 'action', 'is_error', 'static_user_id', 'user_email', 'user_name', 'system_version', 'created',
    )
    search_fields = ('section', 'action', 'static_user_id', 'user_email', 'user_name', 'system_version', 'log',)
    ordering_fields = (
        'section', 'action', 'is_error', 'user', 'static_user_id', 'user_email', 'user_name', 'log', 'system_version',
        'created',
    )
