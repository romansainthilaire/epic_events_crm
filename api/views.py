from rest_framework import generics

from events.models import Client, Contract, Event
from api.serializers import ClientSerializer
from api.permissions import HasGroupPermission


class ClientListCreate(generics.ListCreateAPIView):

    serializer_class = ClientSerializer
    permission_classes = [HasGroupPermission]
    required_groups = {
        "GET": ["gestion", "vente", "support"],
        "POST": ["vente"]
    }

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
