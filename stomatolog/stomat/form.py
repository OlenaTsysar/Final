from django import forms
from .models import DoctorCategory, doctors
from django.core.exceptions import ValidationError

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


    class DoctorCategoryForm(forms.Form):
        class Meta:
            model = DoctorCategory
            fields = "__all__"

        def clean_name(self):
            name = self.cleaned_data["name"]
            if len(name) < 3:
                raise ValidationError ("Korotkoe nazvanie")
            return name

class DoctorCreateForm(forms.ModelForm):
    class Meta:
        model = doctors
        fields = "__all__"

        