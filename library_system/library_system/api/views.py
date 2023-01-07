from hashlib import new
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse, HttpResponse
from rest_framework import status

from api.models import Books, Library, LibraryBooks
from api.serializers import BooksSerializer, LibrarySerializer, LibraryBooksSerializer
from api.messages import *


from django.db import connection
import api.queries as q
import json


@csrf_exempt
def health(request):
    if request.method == "GET":
        return HttpResponse(status=status.HTTP_200_OK) 
    return HttpResponse(status=status.HTTP_400_BAD_REQUEST) 
    

@csrf_exempt
def libraries(request):
    if request.method == "GET":
        try:
            data = JSONParser().parse(request)
            page = None
            size = None
            city = None
            if "size" in data:
                size = int(data["size"])
            if "page" in data:
                page = int(data["page"])

            if "city" in data:
                city = data["city"]
                try:
                    libraries = Library.objects.filter(city=city).all()
                    library_serializer = LibrarySerializer(libraries, many=True)

                    items = library_serializer.data
                    if len(items) > 0:
                        if page is not None and size is not None:
                            if page > 0 and size > 0:
                                if len(items) >= page * size:
                                    items = items[(page - 1) * size : page * size]
                        else:
                            page = 1
                            size = 1
                            items = items[(page - 1) * size : page * size]

                    items = [
                        {
                            "libraryUid": item["library_uid"],
                            "name": item["name"],
                            "address": item["address"],
                            "city": item["city"],
                        }
                        for item in items
                    ]

                    result = {
                        "page": page,
                        "pageSize": size,
                        "totalElements": len(items),
                        "items": items,
                    }

                    return JsonResponse(result, safe=False, status=status.HTTP_200_OK)
                except Exception as ex:
                    print(ex)
                    return HttpResponse(status=status.HTTP_404_NOT_FOUND)
            else:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            print(ex)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


def librarybooks(request):
    if request.method == "GET":
        try:
            data = JSONParser().parse(request)
            library_uid = None
            page = 1
            size = 1
            show_all = True
            if "size" in data:
                size = int(data["size"])
            if "page" in data:
                page = int(data["page"])
            if "show_all" in data:
                if data["show_all"] in ["False", "false"]:
                    show_all = False

            if "library_uid" in data:
                library_uid = data["library_uid"]
            else:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

            try:
                return JsonResponse(
                    q.get_library_books(library_uid, page, size, show_all),
                    safe=False,
                    status=status.HTTP_200_OK,
                )
            except Exception as ex:
                print(ex)
                return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as ex:
            print(ex)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def library_info(request):
    if request.method == "GET":
        try:
            data = JSONParser().parse(request)
            if "libraries_list" in data:
                libraries_list = set(data["libraries_list"])
            else:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

            result = {}
            for library_uid in libraries_list:
                libraries = Library.objects.filter(library_uid=library_uid).all()
                library_serializer = LibrarySerializer(libraries, many=True)
                if len(library_serializer.data) > 0:
                    result[library_uid] = library_serializer.data[0]
                else:
                    result[library_uid] = None

            return JsonResponse(result, safe=False, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def book_info(request):
    if request.method == "GET":
        try:
            data = JSONParser().parse(request)
            if "books_list" in data:
                books_list = set(data["books_list"])
            else:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

            result = {}
            for book_uid in books_list:
                books = Books.objects.filter(book_uid=book_uid).all()
                books_serializer = BooksSerializer(books, many=True)
                if len(books_serializer.data) > 0:
                    result[book_uid] = books_serializer.data[0]
                else:
                    result[book_uid] = None

            return JsonResponse(result, safe=False, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def book_available_count(request):
    if request.method == "GET":
        try:
            data = JSONParser().parse(request)
            if all(k in data for k in ["library_uid", "book_uid"]):
                library_uid = data["library_uid"]
                book_uid = data["book_uid"]
            else:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

            try:
                return JsonResponse(
                    q.get_available_count(library_uid, book_uid),
                    safe=False,
                    status=status.HTTP_200_OK,
                )
            except Exception as ex:
                print(ex)
                return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as ex:
            print(ex)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "POST":
        try:
            data = JSONParser().parse(request)
            if all(k in data for k in ["library_uid", "book_uid", "mode"]):
                library_uid = data["library_uid"]
                book_uid = data["book_uid"]
                mode = str(data["mode"])
            else:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

            if mode == "0":  # decrease
                result = q.change_available_count(library_uid, book_uid, 0)
            elif mode == "1":  # increase
                result = q.change_available_count(library_uid, book_uid, 1)
            else:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

            if result:
                return HttpResponse(status=status.HTTP_202_ACCEPTED)
            else:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            print(ex)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def return_book(request):
    if request.method == "PATCH":
        try:
            data = JSONParser().parse(request)
            if all(k in data for k in ["book_uid", "condition"]):
                condition = data["condition"]
                book_uid = data["book_uid"]
            else:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

            try:
                result = q.return_book(book_uid, condition)
                if result:
                    return JsonResponse(
                        result, safe=False, status=status.HTTP_202_ACCEPTED
                    )
                if result is None:
                    return HttpResponse(status=status.HTTP_404_NOT_FOUND)
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
            except Exception as ex:
                print(ex)
                return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as ex:
            print(ex)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
