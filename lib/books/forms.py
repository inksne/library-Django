from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author', 'publisher', 'category', 'description', 'content', 'language', 'published_date']
        labels = {
            'name': 'Название книги',
            'author': 'Автор',
            'publisher': 'Издатель',
            'category': 'Категория',
            'description': 'Описание',
            'content': 'Содержание',
            'language': 'Язык',
            'published_date': 'Дата публикации',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Введите название книги', 'style': 'color: black;'}),
            'author': forms.TextInput(attrs={'placeholder': 'Введите имя автора', 'style': 'color: black;'}),
            'publisher': forms.TextInput(attrs={'placeholder': 'Введите издателя', 'style': 'color: black;'}),
            'category': forms.Select(attrs={'style': 'color: black;'}),
            'description': forms.Textarea(attrs={'placeholder': 'Введите описание', 'style': 'color: black;'}),
            'content': forms.Textarea(attrs={'placeholder': 'Введите содержание', 'style': 'color: black;'}),
            'language': forms.TextInput(attrs={'placeholder': 'Введите язык книги', 'style': 'color: black;'}),
            'published_date': forms.TextInput(attrs={'placeholder': 'ГГГГ-ММ-ДД', 'style': 'color: black;'}),
        }
