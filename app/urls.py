"""
URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/

Examples
--------
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))

"""
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls import include  # , i18n
from django.conf.urls.static import static
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from . import views


# pylint:disable=invalid-name
handler400 = "app.views.error_400"
# pylint:disable=invalid-name
handler403 = "app.views.error_403"
# pylint:disable=invalid-name
handler404 = "app.views.error_404"
# pylint:disable=invalid-name
handler500 = "app.views.error_500"

urlpatterns = [  # i18n.i18n_patterns(
    # re_path(
    #     r"^api-auth/",
    # ),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path("", views.index, name="index"),
    path("csrf", views.csrf, name="csrf"),
    path("health-check", views.health_check, name="health-check"),
    path("session-info", views.session_info, name="session-info"),
    # re_path(r"^", include("app.profiles.urls")),
    re_path(r"^admin/", admin.site.urls),
    # prefix_default_language=True,
]

# if bool(settings.DEBUG):
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
