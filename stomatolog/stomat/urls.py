from django.urls import path
from .views import Home, Doctors, Doctor, Servise, Contacts, Price_page, OurJobs


urlpatterns = [
    path('', Home, name="home_page"),
    path('doctors/', Doctors, name="doctors_page"),
    path('doctors/<str:name>', Doctor, name="doctor_name_page"),
    path('servise/', Servise, name="servise_page"),
    path('contacts/', Contacts, name="contacts_page"),
    path('price/', Price_page, name="price_page"),
    path('our_jobs/', OurJobs, name="our_jobs_page"),

]