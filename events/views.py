from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from events.models import Client, Contract, Event
from events.forms import ClientForm
from events.decorators import allowed_groups


def about(request):
    return render(request, "events/about.html")


def api_doc(request):
    return render(request, "events/api_doc.html")


@login_required
@allowed_groups(["vente", "support"])
def client_list(request):
    if request.user.groups.filter(name="vente").exists():
        clients = Client.objects.filter(sales_contact=request.user)
    elif request.user.groups.filter(name="support").exists():
        events = Event.objects.filter(support_contact=request.user)
        contracts = Contract.objects.filter(event__in=events)
        clients = Client.objects.filter(contracts__in=contracts)
    context = {"clients": clients}
    return render(request, "events/client/client_list.html", context)


@login_required
@allowed_groups(["vente"])
def client_create(request):
    client_form = ClientForm()
    if request.method == "POST":
        client_form = ClientForm(request.POST)
        if client_form .is_valid():
            client = client_form.save(commit=False)
            client.sales_contact = request.user
            client.save()
            return redirect("client_list")
    context = {"client_form": client_form}
    return render(request, "events/client/client_form.html", context)


@login_required
@allowed_groups(["vente"])
def client_update(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.user != client.sales_contact:
        raise PermissionDenied()
    client_form = ClientForm(instance=client)
    if request.method == "POST":
        client_form = ClientForm(request.POST, instance=client)
        if client_form.is_valid():
            client.save()
            return redirect("client_list")
    context = {"client_form": client_form, "client": client}
    return render(request, "events/client/client_form.html", context)


@login_required
@allowed_groups(["vente"])
def contract_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.user != client.sales_contact:
        raise PermissionDenied()
    contracts = Contract.objects.filter(client=client)
    context = {"contracts": contracts, "client": client}
    return render(request, "events/contract/contract_list.html", context)
