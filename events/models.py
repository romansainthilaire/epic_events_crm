from django.db import models
from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField


class Client(models.Model):

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=100, unique=True)
    phone = PhoneNumberField(unique=True)
    mobile = PhoneNumberField(unique=True)
    company_name = models.CharField(max_length=100, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.first_name.capitalize()} {self.last_name.upper()} - {self.company_name.upper()}"


class Contract(models.Model):

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    sales_contact = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100)
    content = models.TextField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_due_date = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    signed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.amount} €"


class Event(models.Model):

    CUSTOMER_SATISFACTION_CHOICES = ((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"))

    contract = models.OneToOneField(Contract, on_delete=models.CASCADE)
    support_contact = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    event_date = models.DateTimeField(null=True)
    attendees = models.SmallIntegerField(null=True)
    event_retrospective = models.TextField()
    customer_satisfaction = models.SmallIntegerField(choices=CUSTOMER_SATISFACTION_CHOICES, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.contract.title} - {self.event_date}"
