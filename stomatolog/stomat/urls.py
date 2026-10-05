from django.urls import path
from .views import Home, Doctors, Doctor_page, Servise, Contacts, Price_page, OurJobs, Order, Create_doctor


urlpatterns = [
    path('', Home, name="home_page"),
    path('doctors/', Doctors, name="doctors_page"),
    path('doctors/<int:id>', Doctor_page, name="doctor_name_page"),
    path('doctors/craete/', Create_doctor, name="create_doctor"),
    path('servise/', Servise, name="servise_page"),
    path('contacts/', Contacts, name="contacts_page"),
    path('price/', Price_page, name="price_page"),
    path('our_jobs/', OurJobs, name="our_jobs_page"),
    path('order/', Order, name="order_page"),

]