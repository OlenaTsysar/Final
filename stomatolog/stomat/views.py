from django.shortcuts import render
from django.http import HttpResponse
from .models import service, Category, Price, DoctorsQualification
from .form import ContactForm

# Create your views here.
def Home(request):
    return render(request, 'stomat/home.html')

def Doctors(request):
    doctor_list = ["alex", "oleg", "dima"]
    return render(request, "stomat/doctors.html", {"doctor_list": doctor_list})

    # def __str__(self):
    #     return print(self.name)

def Doctor(request, name):
    return HttpResponse(f'doctor {name}!')

def Servise(request):
    category_list = Category.objects.all()
    servise_list = service.objects.all()
    context = {
        "category": category_list,
        "service": servise_list
    }
    return render(request, 'stomat/servise.html', context)

def Order(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            return HttpResponse(f"Спасибо, {name}! Мы свяжемся с вами по адресу {email}.")
    else:
        form = ContactForm()

    return render(request, "contacts.html", {"form": form})


def Price_page(request):
    category_list = Category.objects.all()
    price_list = Price.objects.all()
    context = {
        "category": category_list,
        "price": price_list
    }
    return render(request, 'stomat/price.html', context)

def OurJobs(request):
    return HttpResponse('our_jobs')

def Contacts(request):
    return render(request, 'stomat/contacts.html')
