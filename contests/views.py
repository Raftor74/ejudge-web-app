from django.shortcuts import render
from .classes import ContestsManager


def index(request):
    manager = ContestsManager()
    info = manager.upload_xml_info()
    return render(request, 'contests/index.html', {'info':info})