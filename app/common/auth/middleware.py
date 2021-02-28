import traceback

from django.utils.functional import SimpleLazyObject
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from django.conf import LazySettings
from django.contrib.auth.middleware import get_user
from ..models import User
from .tokens import decode_token


settings = LazySettings()


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: self.__class__.get_jwt_user(request))

    @staticmethod
    def get_jwt_user(request):
        user = get_user(request)

        if user.is_authenticated:
            return user

        token = request.META.get("HTTP_AUTHORIZATION", None)

        if token is None:
            return AnonymousUser()

        try:
            if not token.startswith("Bearer "):
                raise ValueError("Token format is invalid")

            user_jwt = decode_token(token[7:])
            user = User.objects.get(username=user_jwt["username"])

            return user
        except Exception as exc:  # NoQA
            traceback.print_exc()
