from rest_framework import serializers
from . models import *
  
class ReactSerializer(serializers.ModelSerializer):
    class Meta:
        model = React
        fields = ['albumart', 'artists', 'duration', 'name', 'preview_url', 'track_number', 'uri']