from django.shortcuts import render
from django.http import HttpResponse
from .models import service, Category, Price, DoctorsQualification, doctors, DoctorCategory, Date, ourJobs
from .form import OrderForm, DoctorCreateForm, DateForm, DoctorUpdateForm
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy




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
    if request.method == "GET":
        form = OrderForm()
        date_form = DateForm()
        return render(request, "stomat/order.html", {"form": form, "date_form": date_form})

    if request.method == "POST":
       
        form = OrderForm(request.POST)
        date_form = DateForm(request.POST)

        if form.is_valid() and date_form.is_valid():
            
            rezerv = date_form.cleaned_data['date']
            rezerv.is_buzy = True
            rezerv.save()     
            
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            telefon = form.cleaned_data["telefon"]
  
            
            form = OrderForm()
            date_form = DateForm()
            # return render(request, "stomat/order.html", {"form": form})
    else:
        form = OrderForm()
        date_form = DateForm()

    return render(request, "stomat/order.html", {"form": form,
                                                 "date_form": date_form})

    # return HttpResponse('order')

# def Date_oder (request):

#     if request.method == "POST":
#         date_form = DateForm(request.POST)

#         print(date_form.fields["date"].queryset)
#         if date_form.is_valid():
#             rezerv = date_form.cleaned_data['date']
#             rezerv.is_buzy = True
#             rezerv.save()           
#             date_form = DateForm()

#     else:
#         date_form = DateForm()

#     return render(request, "stomat/order.html", {"date_form": date_form})


def Price_page(request):
    category_list = Category.objects.all()
    price_list = Price.objects.all()
    context = {
        "category": category_list,
        "price": price_list
    }
    return render(request, 'stomat/price.html', context)

# def OurJobs(request):
#     return HttpResponse('our_jobs')

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

class OurJobsListView(ListView):
    model = ourJobs;
    template_name = 'stomat/our_jobs.html'
    context_object_name = "jobs"
    paginate_by = 1

class DoctorsUpdateView(UpdateView):
    model = doctors
    form_class = DoctorUpdateForm
    template_name = "stomat/update_doctor.html"
    success_url = reverse_lazy ("doctors_page")
    pk_url_kwarg = 'id'


class DoctorDeleteView(DeleteView):
    model = doctors
    template_name = "stomat/doctor_confirm_delete.html"
    success_url = reverse_lazy("doctors_page")
    pk_url_kwarg = 'id'