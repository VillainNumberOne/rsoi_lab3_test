from pyexpat import model
from rest_framework import serializers
from api.models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("id", "reservation_uid", "username", "book_uid", "library_uid", "status", "start_date", "till_date")