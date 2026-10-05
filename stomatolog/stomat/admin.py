from django.contrib import admin
from .models import service, Category, doctors, DoctorCategory, Price,DoctorsQualification, order

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'description')
    search_fields = ('name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','description')
    search_fields = ('name',)

class DoctorCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class DoctorsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'experience', 'category', 'photo', 'description')
    search_fields = ('name',)

class DoctorsQualificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image')
    search_fields = ('name',)

class PriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'price')
    search_fields = ('name',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'data', 'data_is_stock', 'time', 'time_is_stock')

# Register your models here.
admin.site.register(service, ServiceAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(doctors, DoctorsAdmin)
admin.site.register(DoctorCategory, DoctorCategoryAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(DoctorsQualification, DoctorsQualificationAdmin)
admin.site.register(order, OrderAdmin)
