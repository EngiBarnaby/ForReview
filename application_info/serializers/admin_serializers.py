from rest_framework import serializers

from application_info.models import PostTopic
from application_info.models import Post
from application_info.models import PostImg
from application_info.models import Review
from application_info.models import ReviewImg
from application_info.models import SystemConfig
from application_info.models import Log


class PostTopicAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTopic
        fields = '__all__'


class PostAdminSerializer(serializers.ModelSerializer):
    _topic = serializers.SlugRelatedField(read_only=True, slug_field='name', source='topic')
    article = serializers.CharField(write_only=True)

    class Meta:
        model = Post
        fields = (
            'topic', '_topic', 'name', 'img', 'short_text', 'article', 'publication_time', 'saw_users', 'is_faq',
            'is_notify', 'is_news',
        )


class PostImgAdminSerializer(serializers.ModelSerializer):
    _post = serializers.SlugRelatedField(read_only=True, slug_field='name', source='post')

    class Meta:
        model = PostImg
        fields = '__all__'


class ReviewAdminSerializer(serializers.ModelSerializer):
    _user = serializers.SlugRelatedField(read_only=True, slug_field='name', source='user')

    class Meta:
        model = Review
        fields = '__all__'


class ReviewImgAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImg
        fields = '__all__'


class SystemConfigAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemConfig
        fields = '__all__'


class LogAdminSerializer(serializers.ModelSerializer):
    _user = serializers.SlugRelatedField(read_only=True, slug_field='name', source='user')

    class Meta:
        model = Log
        fields = '__all__'
