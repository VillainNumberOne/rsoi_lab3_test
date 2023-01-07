from pyexpat import model
from rest_framework import serializers
from api.models import Rating

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("id", "username", "stars")

