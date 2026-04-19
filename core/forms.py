from django import forms
from .models import Order
from .models import PaymentProof

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'service', 'description', 'room_no', 'referral_code', 'reference_image']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'service': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 3}),
            'room_no': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'referral_code': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            # Note: File inputs don't usually use classes like 'w-full' the same way, but we'll style it in the template
        }

class PaymentProofForm(forms.ModelForm):
    class Meta:
        model = PaymentProof
        fields = ['transaction_id', 'screenshot']
        widgets = {
            'transaction_id': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Enter Transaction ID'}),
        }