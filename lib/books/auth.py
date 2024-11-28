from rest_framework.views import APIView 
from django.shortcuts import render
from django.contrib.auth import authenticate 
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware.csrf import get_token
from rest_framework.exceptions import AuthenticationFailed


class LoginAPIView(APIView):
    def get(self, request, *args, **kwargs):
        context = {
            'title': 'Логин',
        }
        return render(request, 'login.html', context)    

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            response = Response({"message": "Успешный вход"})
            
            response.set_cookie(
                key="access_token",
                value=str(refresh.access_token),
                httponly=False,
                secure=False, 
                samesite="Lax",
            )
            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=False,
                secure=False, 
                samesite="Lax",
            )
            

            response.data['csrf_token'] = get_token(request)
            return response

        return Response({"error": "Невалидные данные"}, status=401)
    

class LogoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response({"message": "Успешный выход"})
        
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
    

class RefreshAccessTokenAPIView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({"error": "Refresh токен не предоставлен"}, status=400)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            response = Response({"access_token": access_token}, status=200)
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=False, 
                secure=False,   
                samesite="Lax"
            )
            return response
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=401)
        except Exception as e:
            return Response({"error": "Невалидный refresh токен"}, status=401)