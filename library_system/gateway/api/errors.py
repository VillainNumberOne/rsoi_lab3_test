def reservations_no_username():
    return {"message": "No Username", "errors": []}


def reservations_error(message):
    return {"message": message, "errors": []}


def return_error(message):
    return {"message": message}
