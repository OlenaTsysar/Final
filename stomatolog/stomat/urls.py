from django.urls import path
from .views import Home, Doctors, Doctor_page, Servise, Contacts, Price_page, OurJobsListView, Order, Create_doctor, DoctorsUpdateView, DoctorDeleteView, DoctorsView, OrderView, RegisterView, LoginView, LogoutView, free_times_ajax, UserOrderView, FAQListView, ReviewListView, ReviewCreateView, QuestionAsk, PriceCreateView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView, PriceUpdateView, PriceDeleteView


urlpatterns = [
    path('', Home, name="home_page"),
    path('doctors/', DoctorsView.as_view(), name="doctors_page"),
    path('doctors/<int:id>', Doctor_page, name="doctor_name_page"),
    path('doctors/create/', Create_doctor, name="create_doctor"),
    path('doctors/update/<int:id>', DoctorsUpdateView.as_view(), name="update_doctor"),
    path('doctors/delete/<int:id>', DoctorDeleteView.as_view(), name="delete_doctor"),
    path('servise/', Servise, name="servise_page"),
    path('contacts/', Contacts, name="contacts_page"),
    path('price/', Price_page, name="price_page"),
    path('price/create/', PriceCreateView.as_view(), name="price_create_page"),
    path('price/update/<int:id>', PriceUpdateView.as_view(), name="price_update_page"),
    path('price/delete/<int:id>', PriceDeleteView.as_view(), name="price_delete_page"),
    path('category/create/', CategoryCreateView.as_view(), name="category_create_page"),
    path('category/update/<int:id>', CategoryUpdateView.as_view(), name="category_update_page"),
    path('category/delete/<int:id>', CategoryDeleteView.as_view(), name="category_delete_page"),
    path('our_jobs/', OurJobsListView.as_view(), name="our_jobs_page"),
    path('order/', OrderView, name="order_page"),
    path('user_orders/', UserOrderView.as_view(), name="user_orders"),
    path("free-times/", free_times_ajax, name="free_times_ajax"),
    path('register/', RegisterView.as_view(), name="register_page"),
    path('login/', LoginView.as_view(), name="login_page"),
    path('logout/', LogoutView.as_view(), name="logout_page"),
    path('FAQ/', FAQListView.as_view(), name="FAQ_page"),
    path('questionAsk/', QuestionAsk, name="questionAsk_page"),
    path('review/', ReviewListView.as_view(), name="review_page"),
    path('review/create/', ReviewCreateView.as_view(), name="review_create"),


]