from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from events.models import Client, Contract, Event


def about(request):
    return render(request, "events/about.html")


def api_doc(request):
    return render(request, "events/api_doc.html")


@login_required
def client_list(request):
    if request.user.groups.filter(name="vente").exists():
        clients = Client.objects.filter(sales_contact=request.user)
    elif request.user.groups.filter(name="support").exists():
        events = Event.objects.filter(support_contact=request.user)
        contracts = Contract.objects.filter(event__in=events)
        clients = Client.objects.filter(contracts__in=contracts)
    else:
        raise PermissionDenied()
    context = {"clients": clients}
    return render(request, "events/client/client_list.html", context)
