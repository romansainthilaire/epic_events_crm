from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied

from events.models import Client, Contract, Event
from api.serializers import ClientSerializer, ContractSerializer
from api.permissions import HasGroupPermission


class ClientListCreate(generics.ListCreateAPIView):

    serializer_class = ClientSerializer
    permission_classes = [HasGroupPermission]
    required_groups = {
        "GET": ["gestion", "vente", "support"],
        "POST": ["vente"]
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


class ClientRetrieveUpdate(generics.RetrieveUpdateAPIView):

    serializer_class = ClientSerializer
    permission_classes = [HasGroupPermission]
    required_groups = {
        "GET": ["gestion", "vente", "support"],
        "PUT": ["vente"],
        "PATCH": ["vente"]
    }
    lookup_url_kwarg = "client_id"

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


class ContractListCreate(generics.ListCreateAPIView):

    serializer_class = ContractSerializer
    permission_classes = [HasGroupPermission]
    required_groups = {
        "GET": ["gestion", "vente", "support"],
        "POST": ["vente"]
    }
    filter_backends = [filters.SearchFilter]
    search_fields = ["client__first_name", "client__last_name", "client__email", "amount"]

    def get_queryset(self):
        client = get_object_or_404(Client, pk=self.kwargs["client_id"])
        group = self.request.user.groups.first().name
        if group == "vente" and client.sales_contact != self.request.user:
            raise PermissionDenied("Vous n'êtes pas responsable de ce client.")
        elif group == "support":
            events = Event.objects.filter(support_contact=self.request.user)
            contracts = Contract.objects.filter(event__in=events)
            clients = Client.objects.filter(contracts__in=contracts)
            if client not in clients:
                raise PermissionDenied("Ce client n'est pas associé à un évènement dont vous êtes responsable.")
        return Contract.objects.filter(client=client)

    def perform_create(self, serializer):
        client = get_object_or_404(Client, pk=self.kwargs["client_id"])
        if client.sales_contact != self.request.user:
            raise PermissionDenied("Vous n'êtes pas responsable de ce client.")
        else:
            serializer.save(client=client)
