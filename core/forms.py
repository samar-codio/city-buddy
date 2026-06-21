from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Order
from .models import PaymentProof


AUTH_INPUT_CLASSES = 'w-full rounded-xl border border-slate-700 bg-slate-950/70 px-4 py-3 text-slate-100 placeholder:text-slate-500 focus:border-cyan-400 focus:outline-none focus:ring-4 focus:ring-cyan-400/10'
FORM_INPUT_CLASSES = 'w-full rounded-xl border border-slate-700 bg-slate-950/70 px-4 py-3 text-slate-100 placeholder:text-slate-500 focus:border-cyan-400 focus:outline-none focus:ring-4 focus:ring-cyan-400/10'


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label='Gmail',
        widget=forms.EmailInput(attrs={
            'class': AUTH_INPUT_CLASSES,
            'placeholder': 'you@gmail.com',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': AUTH_INPUT_CLASSES,
                'placeholder': 'Choose a username',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': AUTH_INPUT_CLASSES,
            'placeholder': 'Create a password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': AUTH_INPUT_CLASSES,
            'placeholder': 'Repeat your password',
        })

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if not email.endswith('@gmail.com'):
            raise ValidationError('Please use a Gmail address for this demo.')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('An account with this Gmail already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            profile = user.profile
            profile.full_name = user.username
            profile.contact = ''
            profile.alt_contact = ''
            profile.save()

        return user


class StyledAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username or Gmail', widget=forms.TextInput(attrs={
        'class': AUTH_INPUT_CLASSES,
        'placeholder': 'username or you@gmail.com',
        'autofocus': True,
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': AUTH_INPUT_CLASSES,
        'placeholder': 'Password',
    }))

    def clean(self):
        identifier = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if identifier is not None and password:
            username = identifier
            if '@' in identifier:
                user = User.objects.filter(email__iexact=identifier).first()
                if user:
                    username = user.get_username()

            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password,
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'phone_number', 'alt_phone_number', 'description', 'room_no', 'reference_image']
        widgets = {
            'name': forms.TextInput(attrs={'class': FORM_INPUT_CLASSES, 'placeholder': 'Your full name'}),
            'description': forms.Textarea(attrs={'class': FORM_INPUT_CLASSES, 'rows': 3, 'placeholder': 'What do you need delivered or handled?'}),
            'room_no': forms.TextInput(attrs={'class': FORM_INPUT_CLASSES, 'placeholder': 'Room, hostel, or delivery point'}),
            'phone_number': forms.TextInput(attrs={'class': FORM_INPUT_CLASSES, 'placeholder': 'Primary phone number'}),
            'alt_phone_number': forms.TextInput(attrs={'class': FORM_INPUT_CLASSES, 'placeholder': 'Alternate phone number'}),
            'reference_image': forms.ClearableFileInput(attrs={'class': 'w-full rounded-xl border border-dashed border-slate-700 bg-slate-950/70 px-4 py-3 text-sm text-slate-300 file:mr-4 file:rounded-lg file:border-0 file:bg-cyan-400 file:px-4 file:py-2 file:text-sm file:font-bold file:text-slate-950 hover:border-cyan-400/60'}),
        }


class PaymentProofForm(forms.ModelForm):
    class Meta:
        model = PaymentProof
        fields = ['transaction_id', 'screenshot']
        widgets = {
            'transaction_id': forms.TextInput(attrs={'class': FORM_INPUT_CLASSES, 'placeholder': 'Enter transaction ID'}),
            'screenshot': forms.ClearableFileInput(attrs={'class': 'w-full rounded-xl border border-dashed border-slate-700 bg-slate-950/70 px-4 py-3 text-sm text-slate-300 file:mr-4 file:rounded-lg file:border-0 file:bg-emerald-400 file:px-4 file:py-2 file:text-sm file:font-bold file:text-slate-950 hover:border-emerald-400/60'}),
        }
