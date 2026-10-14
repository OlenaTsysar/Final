from django.urls import path
from .views import Home, Doctors, Doctor_page, Servise, Contacts, Price_page, OurJobsListView, Order, Create_doctor, DoctorsUpdateView, DoctorDeleteView


urlpatterns = [
    path('', Home, name="home_page"),
    path('doctors/', Doctors, name="doctors_page"),
    path('doctors/<int:id>', Doctor_page, name="doctor_name_page"),
    path('doctors/create/', Create_doctor, name="create_doctor"),
    path('doctors/update/<int:id>', DoctorsUpdateView.as_view(), name="update_doctor"),
    path('doctors/delete/<int:id>', DoctorDeleteView.as_view(), name="delete_doctor"),
    path('servise/', Servise, name="servise_page"),
    path('contacts/', Contacts, name="contacts_page"),
    path('price/', Price_page, name="price_page"),
    path('our_jobs/', OurJobsListView.as_view(), name="our_jobs_page"),
    path('order/', Order, name="order_page"),

]