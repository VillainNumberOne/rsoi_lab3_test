from hashlib import new
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse, HttpResponse
from rest_framework import status

# from api.serializers import PersonSerializer
from api.messages import *

import api.services_requests
import api.utils.utils as utils
import api.errors as errors


@csrf_exempt
def health(request):
    if request.method == "GET":
        return HttpResponse(status=status.HTTP_200_OK) 
    return HttpResponse(status=status.HTTP_400_BAD_REQUEST) 


@csrf_exempt
def libraries(request, library_uid=None):
    if request.method == "GET":
        if library_uid is None:
            try:
                page = 1
                size = 1
                city = None
                if "size" in request.GET:
                    size = request.GET["size"]
                if "page" in request.GET:
                    page = request.GET["page"]
                if page is None or size is None:
                    page = None
                    size = None

                if "city" in request.GET:
                    city = request.GET["city"]
                    try:
                        libraries_data = api.services_requests.get_city_libraries(
                            city, page, size
                        )
                        if libraries_data is None:
                            return JsonResponse({"message": "Bonus Service unavailable"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
                        return JsonResponse(
                            libraries_data, safe=False, status=status.HTTP_200_OK
                        )
                    except Exception as ex:
                        print(ex, flush=True)
                        return HttpResponse(status=status.HTTP_418_IM_A_TEAPOT)
                else:
                    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
            except:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        else:
            page = 1
            size = 1
            show_all = True
            if "size" in request.GET:
                size = request.GET["size"]
            if "page" in request.GET:
                page = request.GET["page"]
            if "showAll" in request.GET:
                show_all = request.GET["showAll"]

            try:
                librarybooks = api.services_requests.get_library_books(
                    library_uid, page, size, show_all
                )
                if librarybooks is None:
                    return JsonResponse({"message": "Bonus Service unavailable"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
                return JsonResponse(librarybooks, safe=False, status=status.HTTP_200_OK)
            except Exception as ex:
                print(ex)
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def reservations(request):
    if request.method == "GET":
        headers = utils.get_http_headers(request)
        if "X_USER_NAME" in headers.keys():
            username = headers["X_USER_NAME"]
            try:
                reservations = api.services_requests.get_user_reservations(username)
            except Exception as ex:
                print(ex, flush=True)
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
            if reservations is None:
                return JsonResponse({"message": "Bonus Service unavailable"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            return JsonResponse(reservations, safe=False, status=status.HTTP_200_OK)

    elif request.method == "POST":
        headers = utils.get_http_headers(request)
        if "X_USER_NAME" in headers.keys():
            username = headers["X_USER_NAME"]
        else:
            return JsonResponse(
                errors.reservations_no_username(), status=status.HTTP_400_BAD_REQUEST
            )

        try:
            data = JSONParser().parse(request)
            if all(k in data for k in ["bookUid", "libraryUid", "tillDate"]):
                book_uid = data["bookUid"]
                library_uid = data["libraryUid"]
                till_date = data["tillDate"]
            else:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            print(ex)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        try:
            result, error = api.services_requests.make_reservation(
                username, book_uid, library_uid, till_date
            )
            if error == 500:
                return JsonResponse({"message": "Bonus Service unavailable"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as ex:
            print(ex)
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if result is not None:
            return JsonResponse(result, safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse(
                errors.reservations_error(error),
                safe=False,
                status=status.HTTP_400_BAD_REQUEST,
            )

    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def return_book(request, reservation_uid=None):
    if request.method == "POST":
        if reservation_uid is None:
            HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        headers = utils.get_http_headers(request)
        if "X_USER_NAME" in headers.keys():
            username = headers["X_USER_NAME"]
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        try:
            data = JSONParser().parse(request)
            if all(k in data for k in ["condition", "date"]):
                condition = data["condition"]
                date = data["date"]
            else:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
            if condition not in ["BAD", "GOOD", "EXCELLENT"]:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            print(ex)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        try:
            result, error = api.services_requests.return_book(
                username, reservation_uid, condition, date
            )
        except Exception as ex:
            print(ex)
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if result:
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        else:
            if error == 404:
                return JsonResponse(
                    errors.return_error("Not found"),
                    safe=False,
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                return JsonResponse(
                    errors.return_error(error),
                    safe=False,
                    status=status.HTTP_400_BAD_REQUEST,
                )

    HttpResponse(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def rating(request):
    if request.method == "GET":
        headers = utils.get_http_headers(request)
        if "X_USER_NAME" in headers.keys():
            username = headers["X_USER_NAME"]
            try:
                result = api.services_requests.get_user_rating(username)
                if result is None:
                    return JsonResponse({"message": "Bonus Service unavailable"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
                rating, error = result
                if error:
                    if error == 404:
                        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
                    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
                else:
                    result = {"stars": rating}
                    return JsonResponse(result, safe=False, status=status.HTTP_200_OK)

            except Exception as ex:
                print(ex)
                return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
