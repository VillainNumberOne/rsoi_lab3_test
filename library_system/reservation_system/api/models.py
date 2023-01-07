# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    reservation_uid = models.UUIDField(unique=True, null=False)
    username = models.CharField(max_length=80, null=False)
    book_uid = models.UUIDField(null=False)
    library_uid = models.UUIDField(null=False)
    status = models.CharField(max_length=20, null=False)
    start_date = models.DateTimeField(null=False)
    till_date = models.DateTimeField(null=False)

    class Meta:
        managed = False
        db_table = 'reservation'
