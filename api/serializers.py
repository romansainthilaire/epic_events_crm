from rest_framework import serializers

from events.models import Client, Contract, Event


class ClientSerializer(serializers.ModelSerializer):

    sales_contact_id = serializers.IntegerField(source="sales_contact.id", read_only=True)

    class Meta:
        model = Client
        fields = [
            "id",
            "company_name",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "date_created",
            "date_updated",
            "sales_contact_id"
            ]
        read_only_fields = ["date_created", "date_updated"]


class ContractSerializer(serializers.ModelSerializer):

    client_id = serializers.SlugRelatedField(source="client", slug_field="id", queryset=Client.objects.all())

    class Meta:
        model = Contract
        fields = [
            "id",
            "client_id",
            "title",
            "content",
            "amount",
            "payment_due_date",
            "date_created",
            "date_updated",
            "signed",
            "signed_by"
            ]
        read_only_fields = ["payment_due_date", "date_created", "date_updated", "signed", "signed_by"]


class EventSerializer(serializers.ModelSerializer):

    title = serializers.CharField(source="contract.title", read_only=True)
    contract_id = serializers.IntegerField(source="contract.id", read_only=True)
    support_contact_id = serializers.IntegerField(source="support_contact.id", read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "contract_id",
            "support_contact_id",
            "date",
            "attendees",
            "event_retrospective",
            "customer_satisfaction",
            "date_created",
            "date_updated",
            ]
        read_only_fields = ["date_created", "date_updated"]
