from django.shortcuts import render


def about(request):
    return render(request, "events/about.html")


def api_doc(request):
    return render(request, "events/api_doc.html")
