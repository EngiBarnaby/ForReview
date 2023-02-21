from rest_framework import serializers

from application_info.models import PostTopic
from application_info.models import Post
from application_info.models import Review


class PostTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTopic
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    _topic = serializers.SlugRelatedField(read_only=True, slug_field='name', source='topic')
    viewed = serializers.BooleanField(read_only=True)  # аннотируемое поле

    class Meta:
        model = Post
        fields = ('id', 'topic', '_topic', 'name', 'img', 'short_text', 'publication_time',)


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ('grade', 'text', 'user',)
