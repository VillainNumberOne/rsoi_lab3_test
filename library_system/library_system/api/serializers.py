from pyexpat import model
from rest_framework import serializers
from api.models import Books, Library, LibraryBooks

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ("id", "book_uid", "name", "author", "genre", "condition")

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ("id", "library_uid", "name", "city", "address")

class LibraryBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryBooks
        fields = ("book", "library", "available_count")

