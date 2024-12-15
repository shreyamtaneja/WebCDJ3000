from django.shortcuts import render
from rest_framework.views import APIView
from . models import *
from rest_framework.response import Response
from . serializer import *
  
class ReactView(APIView):
    
    serializer_class = ReactSerializer
  
    def get(self, request):
        song = [[song.albumart, song.artists, song.duration, song.name, song.preview_url, song.track_number, song.uri] for song in React.objects.all()]
        return Response(song)
  
    def post(self, request):
        serializer = ReactSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
