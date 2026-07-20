from django.contrib import admin
from django.http import JsonResponse
from django.urls import path


def index(_request):
    return JsonResponse({"message": "Hello from Wodby Django"})


def healthz(_request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("", index),
    path("healthz", healthz),
    path("admin/", admin.site.urls),
]
