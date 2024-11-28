from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=24)

    def __str__(self):
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=48)
    author = models.CharField(max_length=24, null=True, blank=True)
    publisher = models.CharField(max_length=32, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=128, null=True, blank=True)
    content = models.TextField(null=True)
    published_date = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    language = models.CharField(max_length=10, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class UserBooks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f'{self.user.username} - {self.book.name}'