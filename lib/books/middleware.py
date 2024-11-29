from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.urls import resolve

class JWTAuthCookieMiddleware(MiddlewareMixin):
    def process_request(self, request):

        current_route = resolve(request.path_info).url_name
        if current_route == 'token_refresh':
            return

        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        if access_token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
        elif refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                new_access_token = str(refresh.access_token)

                request.COOKIES['access_token'] = new_access_token
                request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_access_token}'
            except Exception as e:
                print(f"Middleware Error: {e}")
                return JsonResponse({"error": "Невалидный либо истекший refresh токен"}, status=401)