from functools import wraps
from rest_framework_simplejwt.tokens import AccessToken
from django.http import JsonResponse

def jwt_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.COOKIES.get('access_token')
        if not token:
            return JsonResponse({'error': 'Токен отсутствует'}, status=401)

        try:
            AccessToken(token)
        except Exception:
            return JsonResponse({'error': 'Неверный токен'}, status=401)

        return view_func(request, *args, **kwargs)

    return _wrapped_view