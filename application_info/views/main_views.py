from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.http.response import HttpResponse
from django.db import transaction

from application_info.models import PostTopic
from application_info.models import Post
from application_info.models import Review
from application_info.services import AnnotationService
from application_info.services import ReviewService

from application_info.serializers.main_serializers import PostTopicSerializer
from application_info.serializers.main_serializers import PostSerializer
from application_info.serializers.main_serializers import ReviewSerializer


class PostTopicsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PostTopic.objects.all()
    serializer_class = PostTopicSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    permission_classes = (IsAuthenticated,)
    filterset_fields = ('name',)
    search_fields = ('name',)
    ordering_fields = ('name',)


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    permission_classes = (IsAuthenticated,)
    filterset_fields = ('topic', 'name', 'is_faq', 'is_notify', 'is_news',)
    search_fields = ('topic__name', 'name', 'short_text', 'article',)
    ordering_fields = ('topic__name', 'name', 'short_text', 'publication_time', 'is_faq', 'is_notify', 'is_news',)

    def get_queryset(self):
        queryset = self.queryset.filter(publication_time__lte=timezone.localtime(timezone.now()))
        queryset = AnnotationService.annotate_viewed_news(queryset, self.request.user)
        return queryset

    @action(methods=('get',), detail=False)
    def unviewed_count(self, request):
        return Response({'count': self.filter_queryset(self.get_queryset()).filter(viewed=False).count()})

    @action(methods=('get',), detail=True)
    def read(self, request, pk=None):
        return HttpResponse(mark_safe(self.get_object().article))


class ReviewViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)
    service = ReviewService

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save()
        self.service.add_images(serializer.instance, self.request.FILES.getlist('images'))
