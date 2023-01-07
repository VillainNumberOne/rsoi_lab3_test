from hashlib import new
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse, HttpResponse
from rest_framework import status

from api.models import  Rating
from api.serializers import  RatingSerializer
from api.messages import *


@csrf_exempt
def health(request):
    if request.method == "GET":
        return HttpResponse(status=status.HTTP_200_OK) 
    return HttpResponse(status=status.HTTP_400_BAD_REQUEST) 
    

@csrf_exempt
def rating_system_api(request, username=None):
    if request.method == "GET":
        if username is None:
            ratings =  Rating.objects.all()
            ratings_serializer =  RatingSerializer(ratings, many=True)
            return JsonResponse(ratings_serializer.data, safe=False, status=status.HTTP_200_OK)
        else:
            try:
                person =  Rating.objects.get(username=username)
                person_serializer =  RatingSerializer(person)
                return JsonResponse(person_serializer.data['stars'], safe=False, status=status.HTTP_200_OK)
            except  Rating.DoesNotExist:
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    elif request.method=='PATCH':
        try:
            update_data = JSONParser().parse(request)
        except:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        try:
            person = Rating.objects.get(username=username)
        except Rating.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)


        if {"mode", "amount"} <= update_data.keys():
            mode = int(update_data["mode"])
            amount = update_data["amount"]
            if mode in (0, 1):
                updated_person = RatingSerializer(person).data
                if mode == 1:
                    updated_person["stars"] = min(100, updated_person["stars"] + amount)
                else:
                    updated_person["stars"] = max(0, updated_person["stars"] - amount)

                person_serializer = RatingSerializer(person, data=updated_person)
                if person_serializer.is_valid():
                    person_serializer.save()
                    return HttpResponse(status=status.HTTP_202_ACCEPTED)
                else:
                    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
            else:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
            
    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)