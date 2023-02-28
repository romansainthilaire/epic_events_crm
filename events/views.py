from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def about(request):
    return render(request, "events/about.html")


def api_doc(request):
    return render(request, "events/api_doc.html")


@login_required
def client_list(request):
    return render(request, "events/client/client_list.html")
