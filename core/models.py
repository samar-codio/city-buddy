from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name   = models.CharField(max_length=150)
    contact     = models.CharField(max_length=20)
    alt_contact = models.CharField(max_length=20, blank=True)
    def __str__(self):
        return f"{self.full_name} ({self.user.email})"



class OrderFieldConfig(models.Model):
    FIELD_TYPE_CHOICES = [
        ('text',     'Short Text'),
        ('textarea', 'Long Text'),
        ('number',   'Number'),
    ]
    field_key   = models.SlugField(max_length=50, unique=True,
                    help_text="Internal name, no spaces (e.g. room_no, referral_code)")
    label       = models.CharField(max_length=100,
                    help_text="Label shown to user on the form (e.g. 'Room Number')")
    field_type  = models.CharField(max_length=20, choices=FIELD_TYPE_CHOICES, default='text')
    is_enabled  = models.BooleanField(default=True,
                    help_text="Uncheck to hide this field from the order form")
    is_required = models.BooleanField(default=False,
                    help_text="Check to make this field mandatory")
    order       = models.PositiveIntegerField(default=0,
                    help_text="Controls display order on the form (lower = higher)")
    class Meta:
        ordering = ['order']
    def __str__(self):
        status = "✅" if self.is_enabled else "❌"
        return f"{status} {self.label} ({self.field_key})"




class Order(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('paid',      'Paid'),
        ('completed', 'Completed'),
    ]
    SERVICE_CHOICES = [
        ('printing',   'Printing'),
        ('binding',    'Binding'),
        ('lamination', 'Lamination'),
        ('photocopy',  'Photocopy'),
        ('other',      'Other'),
    ]
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    name        = models.CharField(max_length=150)
    service     = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    description = models.TextField(blank=True)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at  = models.DateTimeField(auto_now_add=True)
    # Optional built-in fields (shown/hidden by OrderFieldConfig)
    room_no       = models.CharField(max_length=20, blank=True)
    referral_code = models.CharField(max_length=50, blank=True)
    # Extra dynamic fields stored as JSON
    # Stores answers for any custom fields admin creates
    extra_data    = models.JSONField(default=dict, blank=True)
    def __str__(self):
        return f"Order #{self.pk} — {self.name} [{self.status}]"
    class Meta:
        ordering = ['-created_at']


class PaymentProof(models.Model):
    order          = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    transaction_id = models.CharField(max_length=100, blank=True)
    screenshot     = models.ImageField(upload_to='payment_proofs/', blank=True, null=True)
    submitted_at   = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Payment for Order #{self.order.pk}"


class Offer(models.Model):
    title       = models.CharField(max_length=200)
    description = models.TextField()
    image       = models.ImageField(upload_to='offers/')
    is_active   = models.BooleanField(default=True)
    def __str__(self):
        return self.title


class Banner(models.Model):
    image     = models.ImageField(upload_to='banners/')
    caption   = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.caption or f"Banner #{self.pk}"