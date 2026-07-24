from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    """Render the starter landing page."""
    return render(request, "core/index.html")


def healthz(_request):
    """Report that the Django application can serve requests."""
    return JsonResponse({"status": "ok"})
