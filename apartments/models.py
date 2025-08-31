from django.db import models
from django.utils import timezone

# Create your models here.


class Apartment(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    number_of_units = models.PositiveIntegerField(default=0)
    number_of_current_tenants = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Unit(models.Model):
    STATUS_CHOICES = [
        ('vacant', 'Vacant'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
    ]

    apartment = models.ForeignKey(
        Apartment, related_name='units', on_delete=models.CASCADE)
    floor = models.PositiveIntegerField()
    max_tenants = models.PositiveIntegerField(default=1)
    unit_price = models.FloatField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='vacant')

    def calculate_total_rent(self):
        # Base Rent
        total = self.unit_price

        # Add fixed water bill
        Water_Bill = 150
        total += Water_Bill

        # Add latest electricity bill if available
        latest_reading = self.meter_readings.order_by('-reading_date').first()
        if latest_reading:
            total += latest_reading.calculate_bill()

        # For Visitors Charge Logic
        total += self.visitors.filter(
            visit_date__month=timezone.now().month
        ).count() * 50
        # Assuming a fixed charge per visitor

        return total

    def __str__(self):
        return f"Unit {self.id} in {self.apartment.name}"


class Tenant(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=11)
    date_of_birth = models.DateField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    original_address = models.TextField()
    email = models.EmailField(unique=True)

    unit = models.ForeignKey(
        Unit, related_name='tenants', on_delete=models.CASCADE)
    move_in_date = models.DateField(auto_now_add=True)
    move_out_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class VisitorLog(models.Model):
    tenant = models.ForeignKey(
        Tenant, related_name='visitor_logs', on_delete=models.CASCADE
    )
    unit = models.ForeignKey(
        Unit, related_name='visitors', on_delete=models.CASCADE, null=True, blank=True
    )
    visitor_name = models.CharField(max_length=100)
    visitor_contact = models.CharField(max_length=15)
    visit_date = models.DateTimeField(auto_now_add=True)
    purpose_of_visit = models.TextField()


class MeterReading(models.Model):
    unit = models.ForeignKey(
        Unit, related_name='meter_readings', on_delete=models.CASCADE)
    month = models.DateField(
        help_text="Use the first day of the month to represent the month")
    previous_reading = models.FloatField(max_digits=10, decimal_places=2)
    current_reading = models.FloatField(max_digits=10, decimal_places=2)
    reading_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def calculate_bill(self):
        return (self.current_reading - self.previous_reading) * 11

    def __str__(self):
        return f"Meter Reading for Unit {self.unit} on {self.reading_date}"


class Payment(models.Model):
    PAYMENT_METHOD = [
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('gcash', 'GCash'),
    ]

    tenant = models.ForeignKey(
        Tenant, related_name='payments', on_delete=models.CASCADE)
    unit = models.ForeignKey(
        Unit, related_name='payments', on_delete=models.CASCADE)
    amount = models.FloatField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    payment_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Payment of {self.amount} by {self.tenant.first_name} {self.tenant.last_name} on {self.payment_date}"
