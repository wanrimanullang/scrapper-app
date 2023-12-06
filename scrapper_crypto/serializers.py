from rest_framework import serializers
from .models import RedditTopic, YouTubeVideo

class RedditTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedditTopic
        fields = '__all__'
        
class YouTubeVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = YouTubeVideo
        fields = '__all__'