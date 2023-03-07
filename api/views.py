from rest_framework import generics

from events.models import Client, Contract, Event
from api.serializers import ClientSerializer


class ClientList(generics.ListAPIView):

    serializer_class = ClientSerializer

    def get_queryset(self):
        if self.request.user.groups.exists():
            group = self.request.user.groups.first().name
            if group == "gestion":
                return Client.objects.all()
            elif group == "vente":
                return Client.objects.filter(sales_contact=self.request.user)
            elif group == "support":
                events = Event.objects.filter(support_contact=self.request.user)
                contracts = Contract.objects.filter(event__in=events)
                return Client.objects.filter(contracts__in=contracts).distinct()
        else:
            return Client.objects.none()
