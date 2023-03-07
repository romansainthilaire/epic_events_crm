from rest_framework import serializers

from events.models import Client, Contract


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
            "phone",
            "mobile",
            "date_created",
            "date_updated",
            "sales_contact_id"
            ]
        read_only_fields = ["date_created", "date_updated"]


class ContractSerializer(serializers.ModelSerializer):

    client_id = serializers.IntegerField(source="client.id", read_only=True)

    class Meta:
        model = Contract
        fields = [
            "id",
            "client",
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
        read_only_fields = ["date_created", "date_updated", "signed", "signed_by"]
        extra_kwargs = {"client": {"write_only": True}}
