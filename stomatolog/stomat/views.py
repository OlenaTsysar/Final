from django.shortcuts import render
from django.http import HttpResponse
from .models import service, Category, Price, DoctorsQualification, doctors, DoctorCategory
from .form import ContactForm, DoctorCreateForm

# Create your views here.
def Home(request):
    return render(request, 'stomat/home.html')

def Doctors(request):
    category_list = DoctorCategory.objects.all()
    doctor_list = doctors.objects.all()
    context = {"category": category_list,
        "doctors": doctor_list}
    return render(request, "stomat/doctors.html", context)

    # def __str__(self):
    #     return print(self.name)

def Doctor_page(request, id):
    context = {}
    try:
        doc = doctors.objects.get(id=id)
        context["doc"] = doc
    except doctors.DoesNotExist:
        context["doc"] = None
    return render(request, 'stomat/doctor.html', context)

def Servise(request):
    category_list = Category.objects.all()
    servise_list = service.objects.all()
    context = {
        "category": category_list,
        "service": servise_list
    }
    return render(request, 'stomat/servise.html', context)

def Order(request):
    return HttpResponse('order')


    # if request.method == "POST":
    #     form = ContactForm(request.POST)
    #     if form.is_valid():
    #         name = form.cleaned_data["name"]
    #         email = form.cleaned_data["email"]
    #         return HttpResponse(f"Спасибо, {name}! Мы свяжемся с вами по адресу {email}.")
    # else:
    #     form = ContactForm()

    # return render(request, "contacts.html", {"form": form})


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

def Create_doctor(request):
    if request.method == "GET":
        form = DoctorCreateForm()
        return render(request, "stomat/create_doctor.html", {"form": form})
    
    if request.method == "POST":
        form = DoctorCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = DoctorCreateForm()
        return render(request, "stomat/create_doctor.html", {"form": form})