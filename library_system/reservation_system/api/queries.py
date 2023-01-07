from django.db import connection
import uuid
from datetime import datetime


def get_rented_count(username):
    query = f"""
select count(id) from reservation 
where status = 'RENTED'
and username = '{username}'
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        fetched = cursor.fetchall()

    if len(fetched) == 0:
        return 0
    else:
        return fetched[0][0]


def make_reservation(username, book_uid, library_uid, start_date, till_date):
    uid = str(uuid.uuid4())
    query = f"""
insert into reservation (reservation_uid, username, book_uid, library_uid, status, start_date, till_date)
values ('{uid}', '{username}', '{book_uid}', '{library_uid}', 'RENTED', '{start_date}', '{till_date}')
    """

    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            connection.commit()
            result = True
        except Exception as ex:
            print(ex)
            connection.rollback()
            result = False

    if result:
        result = {
            "reservationUid": uid,
            "status": "RENTED",
            "startDate": start_date,
            "tillDate": till_date,
        }

    return result


def return_book(username, reservation_uid, date):
    query = f"""
select * from reservation
where reservation_uid = '{reservation_uid}'
and username = '{username}'
and status = 'RENTED'
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        fetched = cursor.fetchall()

    items = [
        {
            "id": row[0],
            "reservation_uid": str(row[1]),
            "username": row[2],
            "book_uid": row[3],
            "library_uid": row[4],
            "status": row[5],
            "start_date": row[6],
            "till_date": row[7],
        }
        for row in fetched
    ]
    if len(items) == 0:
        return None
    items = items[0]

    status = "RETURNED" if items["till_date"] >= datetime.strptime(date, "%Y-%m-%d") else "EXPIRED"
    items['status'] = status
    query = f"""
update reservation set status = '{status}'
where reservation_uid = '{reservation_uid}'
    """

    result = True
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            connection.commit()
            if cursor.rowcount == 0:
                result = False
        except Exception as ex:
            print(ex)
            connection.rollback()
            result = False

    return items if result else False
