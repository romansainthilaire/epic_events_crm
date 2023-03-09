import datetime

from django.shortcuts import get_object_or_404

from rest_framework import mixins, viewsets, filters, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response

from events.models import Client, Contract, Event
from api.serializers import ClientSerializer, ContractSerializer, EventSerializer
from api.permissions import HasGroupPermission


class ClientViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = ClientSerializer
    permission_classes = [HasGroupPermission]
    required_groups = {
        "GET": ["gestion", "vente", "support"],
        "POST": ["vente"],
        "PUT": ["vente"]
    }
    filter_backends = [filters.SearchFilter]
    search_fields = ["first_name", "last_name", "email"]

    def get_queryset(self):
        group = self.request.user.groups.first().name
        if group == "gestion":
            return Client.objects.all()
        elif group == "vente":
            return Client.objects.filter(sales_contact=self.request.user)
        elif group == "support":
            events = Event.objects.filter(support_contact=self.request.user)
            contracts = Contract.objects.filter(event__in=events)
            return Client.objects.filter(contracts__in=contracts).distinct()

    def perform_create(self, serializer):
        serializer.save(sales_contact=self.request.user)


class ContractViewSet(viewsets.ModelViewSet):

    serializer_class = ContractSerializer
    permission_classes = [HasGroupPermission]
    required_groups = {
        "GET": ["gestion", "vente", "support"],
        "POST": ["vente"],
        "PUT": ["vente"],
        "DELETE": ["vente"]
    }
    filter_backends = [filters.SearchFilter]
    search_fields = ["client__first_name", "client__last_name", "client__email", "amount"]

    def get_queryset(self):
        group = self.request.user.groups.first().name
        if group == "gestion":
            return Contract.objects.all()
        elif group == "vente":
            clients = Client.objects.filter(sales_contact=self.request.user)
            return Contract.objects.filter(client__in=clients)
        elif group == "support":
            events = Event.objects.filter(support_contact=self.request.user)
            return Contract.objects.filter(event__in=events)

    def perform_create(self, serializer):
        if serializer.is_valid:
            client = serializer.validated_data["client"]
            if client.sales_contact != self.request.user:
                raise PermissionDenied("Vous n'êtes pas responsable de ce client.")
            payment_due_date = datetime.datetime.now().date() + datetime.timedelta(60)
            serializer.save(payment_due_date=payment_due_date)

    def perform_update(self, serializer):
        if serializer.is_valid:
            client = serializer.validated_data["client"]
            if client.sales_contact != self.request.user:
                raise PermissionDenied("Vous n'êtes pas responsable de ce client.")
            contract = Contract.objects.get(pk=self.kwargs["pk"])
            if contract.signed:
                raise PermissionDenied("Vous ne pouvez pas modifier un contrat signé.")
            payment_due_date = datetime.datetime.now().date() + datetime.timedelta(60)
            serializer.save(payment_due_date=payment_due_date)

    def perform_destroy(self, instance):
        if instance.signed:
            raise PermissionDenied("Vous ne pouvez pas supprimer un contrat signé.")
        instance.delete()


@api_view(["POST"])
def sign_contract(request, contract_id):
    if not request.user.groups.exists() or request.user.groups.first().name != "vente":
        raise PermissionDenied()
    contract = get_object_or_404(Contract, pk=contract_id)
    if contract.client.sales_contact != request.user:
        raise PermissionDenied("Vous n'êtes pas responsable de ce client.")
    if contract.signed:
        raise PermissionDenied("Ce contrat a déjà été signé.")
    contract.signed = True
    contract.signed_by = request.user.first_name.capitalize() + " " + request.user.last_name.upper()
    contract.save()
    event = Event()
    event.contract = contract
    event.save()
    return Response(status=status.HTTP_201_CREATED)


class EventViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):

    serializer_class = EventSerializer
    permission_classes = [HasGroupPermission]
    required_groups = {
        "GET": ["gestion", "vente", "support"],
        "PUT": ["support"]
    }
    filter_backends = [filters.SearchFilter]
    search_fields = ["contract__client__first_name", "contract__client__last_name", "contract__client__email"]

    def get_queryset(self):
        group = self.request.user.groups.first().name
        if group == "gestion":
            return Event.objects.all()
        elif group == "vente":
            contracts = Contract.objects.filter(client__sales_contact=self.request.user).filter(signed=True)
            return Event.objects.filter(contract__in=contracts)
        elif group == "support":
            return Event.objects.filter(support_contact=self.request.user)

    def perform_update(self, serializer):
        if serializer.is_valid:
            date = serializer.validated_data["date"]
            event = Event.objects.get(pk=self.kwargs["pk"])
            contract = Contract.objects.get(event=event)
            if date < contract.date_updated.date():
                raise ValidationError(
                    "L'évènement ne peut pas avoir eu lieu avant la date de signature du contrat (" +
                    contract.date_updated.date().strftime("%d/%m/%y") + ")."
                    )
            if date > datetime.date.today():
                raise ValidationError(
                    "Vous ne pouvez pas rédiger un compte rendu pour un évènement qui n'a pas encore eu lieu."
                    )
            serializer.save()
