import requests
import json
from datetime import datetime
from api.simple_circuit import Circuit

LIBRARY_SYSTEM = "http://librarysystem:8060"
RATING_SYSTEM = "http://ratingsystem:8050"
RESERVATION_SYSTEM = "http://reservationsystem:8070"


#### GET CITY LIBRARIES #####################################################

def health(SYSTEM):
    try:
        status = requests.get(f"{SYSTEM}/manage/health").status_code
        if status != 200:
            raise ConnectionError()
    except Exception:
        raise ConnectionError()


def get_city_libraries_request(data):
    health(LIBRARY_SYSTEM)
    response = requests.get(
        f"{LIBRARY_SYSTEM}/api/v1/libraries", data=json.dumps(data)
    ).text
    return json.loads(response)


def get_city_libraries_fallback(*args, **kwargs):
    return None

#### GET LIBRARY BOOKS #####################################################


def get_library_books_request(data):
    health(LIBRARY_SYSTEM)
    response = requests.get(
        f"{LIBRARY_SYSTEM}/api/v1/librarybooks", data=json.dumps(data)
    ).text
    return json.loads(response)


def get_library_books_fallback(*args, **kwargs):
    return None


#### GET USER RATING #####################################################


def get_user_rating_request(username):
    health(RATING_SYSTEM)
    response = requests.get(f"{RATING_SYSTEM}/api/v1/ratings/{username}")
    if response.status_code != 200:
        return None, response.status_code
    else:
        user_stars = json.loads(response.text)
        return user_stars, None


def get_user_rating_fallback(*args, **kwargs):
    return None


#### GET USER RESERVATIONS #####################################################


def get_reservations_request(username):
    health(RESERVATION_SYSTEM)
    reservations = json.loads(
        requests.get(
            f"{RESERVATION_SYSTEM}/api/v1/reservations/{username}").text
    )
    return reservations


def get_reservations_fallback(*args, **kwargs):
    return None


def get_libraries_books_info_request(libraries_info_data, books_info_data, reservations):
    health(LIBRARY_SYSTEM)
    libraries_info = json.loads(
        requests.get(
            f"{LIBRARY_SYSTEM}/api/v1/libraries/info",
            data=json.dumps(libraries_info_data),
        ).text
    )
    books_info = json.loads(
        requests.get(
            f"{LIBRARY_SYSTEM}/api/v1/books/info", data=json.dumps(books_info_data)
        ).text
    )

    libraries = {
        library_uid: {
            "libraryUid": library_uid,
            "name": library_info["name"],
            "address": library_info["address"],
            "city": library_info["city"],
        }
        for library_uid, library_info in libraries_info.items()
    }

    books = {
        book_uid: {
            "bookUid": book_uid,
            "name": book_info["name"],
            "author": book_info["author"],
            "genre": book_info["genre"],
        }
        for book_uid, book_info in books_info.items()
    }

    result = [
        {
            "reservationUid": reservation["reservation_uid"],
            "status": reservation["status"],
            "startDate": reservation["start_date"],
            "tillDate": reservation["till_date"],
            "book": books[reservation["book_uid"]],
            "library": libraries[reservation["library_uid"]],
        }
        for reservation in reservations
    ]

    return result


def get_libraries_books_info_fallback(libraries_info_data, books_info_data, reservations):
    result = [
        {
            "reservationUid": reservation["reservation_uid"],
            "status": reservation["status"],
            "startDate": reservation["start_date"],
            "tillDate": reservation["till_date"],
            "book": reservation["book_uid"],
            "library": reservation["library_uid"],
        }
        for reservation in reservations
    ]

    return result


#### MAKE RESERVATION #####################################################


def library_rating_health():
    health(LIBRARY_SYSTEM)
    health(RATING_SYSTEM)
    health(RESERVATION_SYSTEM)
    return True


def library_rating_fallback():
    return False


def make_reservation_library_service_request(available_count_data):
    health(LIBRARY_SYSTEM)
    try:
        status_code = requests.post(
            f"{LIBRARY_SYSTEM}/api/v1/books/available",
            data=json.dumps(available_count_data),
        ).status_code
    except Exception:
        status_code = 500
    return status_code


def make_reservation_library_service_fallback(*args, **kwargs):
    return 500


#### CIRCUITS #####################################################


