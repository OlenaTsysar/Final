from django import forms
from .models import DoctorCategory, doctors, DoctorsQualification, Order, Price
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class OrderForm(forms.ModelForm):
    time = forms.ChoiceField(
        choices=[("", "Сначала выберите врача и дату")],
        label="Время",
        widget=forms.Select(attrs={
            "class": "form-control",
            "id": "id_time",
        }),
    )
        
    class Meta:
        model = Order
        fields = ["doctor", "date", "time"]
        widgets = {
            "doctor": forms.Select(attrs={
                "class": "form-control",
                "id": "id_doctor"
            }),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control",
            "id": "id_date"}),
            # "time": forms.TimeInput(attrs={"type": "time", "class": "form-control",
            # "id": "id_time"}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["time"].choices = [
            ("", "Выберите время")
        ] + [
            (f"{hour:02d}:{minute:02d}",
             f"{hour:02d}:{minute:02d}")
            for hour in range(9, 16)
            for minute in (0, 30)
        ]


class DoctorCategoryForm(forms.ModelForm):
        class Meta:
            model = DoctorCategory
            fields = "__all__"

        def clean_name(self):
            name = self.cleaned_data["name"]
            if len(name) < 3:
                raise ValidationError ("Короткое имя")
            return name

class DoctorCreateForm(forms.ModelForm):
    class Meta:
        model = doctors
        fields = "__all__"

class DoctorUpdateForm(forms.ModelForm):
    class Meta:
        model = doctors
        fields = "__all__"


class RegisterForm(forms.Form):
    username = forms.CharField(label="Имя пользователя")
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password1"],
        )
        return user


class LoginForm(forms.Form):
    user_name = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        user_name = cleaned_data.get("user_name")
        password = cleaned_data.get("password")

        if user_name and password:
            self.user = authenticate(username = user_name, password=password)
            if self.user is None:
                raise forms.ValidationError("Неверный логин или пароль")
        return cleaned_data

class QuestionForm(forms.Form):
    name = forms.CharField(label="Имя клиента")
    email = forms.EmailField(label="Email")
    question = forms.CharField(
        label="Ваш вопрос",
        widget=forms.Textarea())

class PriceCreateForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = "__all__"