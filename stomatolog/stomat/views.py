from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from .models import service, Category, Price, DoctorsQualification, doctors, DoctorCategory, ourJobs, Order, FAQ, Review
from .form import OrderForm, DoctorCreateForm, DoctorUpdateForm, OrderForm, LoginForm
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, RedirectView
from django.contrib.auth import login, logout

from datetime import datetime, time, timedelta, date
from django.utils import timezone

from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404



# Create your views here.
def Home(request):
    category = Category.objects.all()
    return render(request, 'stomat/home.html', {'category': category})

def Doctors(request):
    category_list = DoctorCategory.objects.all()
    doctor_list = doctors.objects.all()
    context = {"category": category_list,
        "doctors": doctor_list}
    return render(request, "stomat/doctors.html", context)

class DoctorsView(TemplateView):
    template_name = "stomat/doctors.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = DoctorCategory.objects.prefetch_related("doctors").all()

        # category_list = DoctorCategory.objects.all()
        # doctor_list = doctors.objects.all()

        for category in categories:
            paginator = Paginator(category.doctors.all(), 2)
            page_number = self.request.GET.get(f'page_{category.id}')
            category.page_obj = paginator.get_page(page_number)

        context["category"] = categories

        # context["category"] = category_list
        # context["doctors"] = page_obj
        # context["page_obj"] = page_obj

        return context

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

# def Order(request):
#     if request.method == "GET":
#         form = OrderForm()
    #     # date_form = DateForm()
    #     return render(request, "stomat/order.html", {"form": form})

    # if request.method == "POST":
       
    #     form = OrderForm(request.POST)
    #     # date_form = DateForm(request.POST)

    #     if form.is_valid():

    #         form.save()
            

    #         # rezerv.is_buzy = True
    #         # rezerv.save()     
            
    #         # name = form.cleaned_data["name"]
    #         # email = form.cleaned_data["email"]
    #         # telefon = form.cleaned_data["telefon"]

    #         # date = form.cleaned_data["date"]
    #         # time = form.cleaned_data["time"]
  
            
    #         # form = OrderForm()
    #         # date_form = DateForm()
    #         return render(request, "stomat/order.html", {"form": form})
    # else:
    #     form = OrderForm()
    #     # date_form = DateForm()

    # return render(request, "stomat/order.html", {"form": form})

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

def get_free_times(doctor, selected_date):
    start_work = time(9, 0)
    end_work = time(16, 0)

    work_start = datetime.combine(selected_date, start_work)
    work_end = datetime.combine(selected_date, end_work)

    booked_times = set(
        Order.objects.filter(
            doctor = doctor,
            date = selected_date
        ).values_list("time", flat=True)
    )
    now = timezone.localtime()
    current = work_start
    free_times = []

    while current < work_end:
        slot = current.time()

        if (
            slot not in booked_times 
            and (
                selected_date > now.date() 
                or (
                    selected_date == now.date() and slot > now.time()
                )
            )
        ):
            free_times.append(slot)
        current += timedelta(minutes=30)
    return free_times

@require_GET
def free_times_ajax(request):
    doctor_id = request.GET.get("doctor")
    date_str = request.GET.get("date")

    if not doctor_id or not date_str:
        return JsonResponse({"times": []}, status=400)

    try:
        selected_date = date.fromisoformat(date_str)
    except ValueError:
        return JsonResponse(
            {"error": "Некорректная дата", "times": []},
            status=400,
        )

    doctor = get_object_or_404(doctors, pk=doctor_id)

    times = get_free_times(doctor, selected_date)

    return JsonResponse({
        "times": [slot.strftime("%H:%M") for slot in times]
    })


@login_required
def OrderView(request):
    form = OrderForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        order = form.save(commit=False)
        order.user = request.user

        if order.date < timezone.localdate():
            form.add_error("date", "Нельзя выбрать прошедшую дату.")

        elif order.time not in get_free_times(order.doctor, order.date):
            form.add_error(
                "time",
                "Это время недоступно. Выберите другое."
            )

        else:

            try:
                with transaction.atomic():
                    order.save()
                return redirect("order_page")
            except IntegrityError:
                form.add_error(
                    "time",
                    "Это время уже занято у выбранного врача."
                )
    else:
        form = OrderForm()

    return render(request, "stomat/order.html", {"form": form})

@method_decorator(login_required, name="dispatch")
class UserOrderView(ListView):
    model = Order
    template_name = 'stomat/user_orders.html'
    context_object_name = "user_orders"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related("doctor")


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
    model = ourJobs
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

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "stomat/register.html", {"form": form})

        
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect("home_page")
    else:
        form = LoginForm()
    return render(request, "stomat/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("home_page")

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "stomat/register.html"
    success_url = reverse_lazy("login_page")

class LoginView(FormView):
    form_class = LoginForm
    template_name = "stomat/login.html"
    success_url = reverse_lazy("home_page")

    def form_valid(self, form):
        login(self.request, form.user)
        return super().form_valid(form)

class LogoutView(RedirectView):
    pattern_name = "home_page"

    def post(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)

class FAQListView(ListView):
    model = FAQ
    template_name = 'stomat/FAQ.html'
    context_object_name = "FAQs"
    paginate_by = 2

class ReviewListView(ListView):
    model = Review
    template_name = 'stomat/Review.html'
    context_object_name = "reviews"
    paginate_by = 2