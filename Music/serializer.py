from rest_framework import serializers
from .models import Album, Song


class AlbumListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Album
		fields = ('title', 'artist', 'genre', 'rating')
