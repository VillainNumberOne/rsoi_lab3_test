# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Books(models.Model):
    id = models.IntegerField(primary_key=True)
    book_uid = models.UUIDField(unique=True)
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True, null=True)
    genre = models.CharField(max_length=255, blank=True, null=True)
    condition = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'books'


class Library(models.Model):
    id = models.IntegerField(primary_key=True)
    library_uid = models.UUIDField(unique=True)
    name = models.CharField(max_length=80)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'library'


class LibraryBooks(models.Model):
    book = models.OneToOneField(Books, models.DO_NOTHING, primary_key=True)
    library = models.ForeignKey(Library, models.DO_NOTHING)
    available_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'library_books'
        unique_together = (('book', 'library'),)
