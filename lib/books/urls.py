from django.urls import path, re_path, include
from .views import *
from .auth import *

urlpatterns = [
    path('authenticated/bookslist/', BookAPIView.as_view(), name='bookslist'),
    path('authenticated/bookslist/<int:pk>/', BookAPIUpdateView.as_view()),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('api/v1/logout/', LogoutAPIView.as_view(), name='logout'),
    path('api/v1/token/refresh-cookie/', RefreshAccessTokenAPIView.as_view(), name='token_refresh'),
    path('', BaseView, name='base'),
    path('about_us', AboutUsView, name='about_us'),
    path('authenticated/', BooksView, name='authenticated'),
    path('authenticated/mybooks/', UserBooksView, name='mybooks'),
    path('api/v1/add-to-collection/<int:book_id>/', AddToCollectionAPIView.as_view(), name='add-to-collection'),
    path('register/', RegisterView.as_view(), name='register'),
    path('authenticated/add_book/', AddBooksView.as_view(), name='add_book'),
]
