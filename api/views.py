from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied

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
            contracts = Contract.objects.filter(event__in=events)
            clients = Client.objects.filter(contracts__in=contracts).distinct()
            return Contract.objects.filter(client__in=clients)

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
