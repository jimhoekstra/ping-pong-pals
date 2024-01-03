from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def bad_request(request: HttpRequest) -> HttpResponse:
    return render(request, 'scoreboard/generic/bad_request.html', status=400)
