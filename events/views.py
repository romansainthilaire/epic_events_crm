import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from events.models import Client, Contract, Event
from events.forms import ClientForm, ContractForm, EventForm
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
        clients = Client.objects.filter(contracts__in=contracts).distinct()
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


@login_required
@allowed_groups(["vente"])
def contract_create(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.user != client.sales_contact:
        raise PermissionDenied()
    contract_form = ContractForm()
    if request.method == "POST":
        contract_form = ContractForm(request.POST)
        if contract_form .is_valid():
            contract = contract_form.save(commit=False)
            contract.client = client
            contract.payment_due_date = datetime.datetime.now().date() + datetime.timedelta(60)
            contract.save()
            return redirect("contract_list", client.pk)
    context = {"contract_form": contract_form, "client": client}
    return render(request, "events/contract/contract_form.html", context)


@login_required
@allowed_groups(["vente"])
def contract_update(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    if request.user != contract.client.sales_contact or contract.signed:
        raise PermissionDenied()
    contract_form = ContractForm(instance=contract)
    if request.method == "POST":
        contract_form = ContractForm(request.POST, instance=contract)
        if contract_form.is_valid():
            contract.payment_due_date = datetime.datetime.now().date() + datetime.timedelta(60)
            contract.save()
            return redirect("contract_list", contract.client.pk)
    context = {"contract_form": contract_form, "contract": contract, "client": contract.client}
    return render(request, "events/contract/contract_form.html", context)


@login_required
@allowed_groups(["vente"])
def contract_delete(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    if request.user != contract.client.sales_contact or contract.signed:
        raise PermissionDenied()
    contract.delete()
    return redirect("contract_list", contract.client.pk)


@login_required
@allowed_groups(["vente"])
def contract_sign(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    if request.user != contract.client.sales_contact or contract.signed:
        raise PermissionDenied()
    contract.signed = True
    contract.signed_by = request.user.first_name.capitalize() + " " + request.user.last_name.upper()
    contract.save()
    event = Event()
    event.contract = contract
    event.save()
    return redirect("contract_list", contract.client.pk)


@login_required
@allowed_groups(["vente", "support"])
def event_list(request):
    if request.user.groups.filter(name="vente").exists():
        contracts = Contract.objects.filter(client__sales_contact=request.user).filter(signed=True)
        events = Event.objects.filter(contract__in=contracts)
    elif request.user.groups.filter(name="support").exists():
        events = Event.objects.filter(support_contact=request.user)
    context = {"events": events}
    return render(request, "events/event/event_list.html", context)


@login_required
@allowed_groups(["support"])
def event_update(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.user != event.support_contact:
        raise PermissionDenied()
    event_form = EventForm(instance=event)
    if request.method == "POST":
        event_form = EventForm(request.POST, instance=event)
        if event_form.is_valid():
            event.save()
            return redirect("event_list")
    context = {"event_form": event_form, "event": event}
    return render(request, "events/event/event_form.html", context)
