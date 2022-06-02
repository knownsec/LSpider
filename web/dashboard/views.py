from django.shortcuts import render

from django.http import JsonResponse


def index(request):
    return JsonResponse({"code": 200, "status": True, "message": "HelloWorld"})
