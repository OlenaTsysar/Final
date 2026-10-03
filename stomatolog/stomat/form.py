from django import forms
from .models import DoctorCategory, doctors

class ContactForm(forms.Form):
    name = forms.CharField(
        label="Ваше имя",
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя'
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваш example@mail.com'
        })
    )
