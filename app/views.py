from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token


async def index(request):
    return HttpResponse(status=200)


async def csrf(request):
    return JsonResponse({"csrfToken": get_token(request)})


async def health_check(request):
    return HttpResponse(status=200)


def session_info(request):
    user = request.user

    return JsonResponse({"loggedin": user.is_authenticated, "user": user.username})


# pylint:disable=unused-argument
def error_400(request, exception):
    return HttpResponse("HTTP 400 Bad Request", status=400)


# pylint:disable=unused-argument
def error_403(request, exception):
    return HttpResponse("HTTP 403 Forbidden", status=403)


# pylint:disable=unused-argument
def error_404(request, exception):
    return HttpResponse("HTTP 404 Page not found", status=404)


def error_500(request):
    return HttpResponse("HTTP 500 Internal Server Error", status=500)
