from hashlib import new
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse, HttpResponse
from rest_framework import status

from api.models import Reservation
from api.serializers import ReservationSerializer
from api.messages import *
import api.queries as q


@csrf_exempt
def health(request):
    if request.method == "GET":
        return HttpResponse(status=status.HTTP_200_OK) 
    return HttpResponse(status=status.HTTP_400_BAD_REQUEST) 


@csrf_exempt
def get_user_reservations(request, username=None):
    if request.method == "GET":
        if username is not None:
            persons = Reservation.objects.filter(username=username).all()
            person_serializer = ReservationSerializer(persons, many=True)
            return JsonResponse(person_serializer.data, safe=False, status=status.HTTP_200_OK)

    return HttpResponse(status=status.HTTP_400_BAD_REQUEST) 

@csrf_exempt
def get_rented(request, username=None):
    if request.method == "GET":
        if username is not None:
            try:
                return JsonResponse(q.get_rented_count(username), safe=False, status=status.HTTP_200_OK)
            except Exception as ex:
                print(ex)
                return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def reservation(request):
    if request.method == "POST":
        try:
            data = JSONParser().parse(request)
            if all(k in data for k in ['username', 'book_uid', 'library_uid', 'start_date', 'till_date']):
                username = data['username']
                book_uid = data['book_uid']
                library_uid = data['library_uid']
                start_date = data['start_date']
                till_date = data['till_date']
            else:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

            try:
                result = q.make_reservation(username, book_uid, library_uid, start_date, till_date)
                if result:
                    return JsonResponse(result, safe=False, status=status.HTTP_201_CREATED)
                else:
                    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

            except Exception as ex:
                print(ex)
                return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as ex:
            print(ex)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    if request.method == "PATCH":
        try:
            data = JSONParser().parse(request)
            if all(k in data for k in ['username', 'reservation_uid', 'date']):
                username = data['username']
                reservation_uid = data['reservation_uid']
                date = data['date']
            else:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

            try:
                result = q.return_book(username, reservation_uid, date)
                if result is None:
                    return HttpResponse(status=status.HTTP_404_NOT_FOUND)
                if result:
                    return JsonResponse(result, safe=False, status=status.HTTP_202_ACCEPTED)
                else:
                    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

            except Exception as ex:
                print(ex)
                return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as ex:
            print(ex)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
            
    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)