from rest_framework import serializers
from .models import RedditTopic

class RedditTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedditTopic
        fields = '__all__'