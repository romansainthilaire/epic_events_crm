from rest_framework import serializers

from events.models import Client


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
