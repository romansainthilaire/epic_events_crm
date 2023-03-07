from django.shortcuts import get_object_or_404

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from events.models import Client, Contract, Event
from api.serializers import ClientSerializer, ContractSerializer
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
        "PUT": ["vente"],
        "PATCH": ["vente"]
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
        "PATCH": ["vente"],
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
            serializer.save()

    def perform_update(self, serializer):
        if serializer.is_valid:
            client = serializer.validated_data["client"]
            if client.sales_contact != self.request.user:
                raise PermissionDenied("Vous n'êtes pas responsable de ce client.")
            contract = Contract.objects.get(pk=self.kwargs["pk"])
            if contract.signed:
                raise PermissionDenied("Vous ne pouvez pas modifier un contrat signé.")
            serializer.save()

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
