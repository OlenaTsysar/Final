from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class DoctorCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class doctors(models.Model):

    name = models.CharField(max_length=60)
    # qualification = models.ForeignKey(DoctorsQualification, on_delete=models.CASCADE, related_name="doctors", null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    experience = models.CharField(max_length=100)
    category = models.ForeignKey(DoctorCategory, on_delete=models.PROTECT, related_name="doctors", null=True, blank=True)
    photo = models.ImageField(upload_to='stomat/image', null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Доктор"
        verbose_name_plural = "Доктора"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize().strip(' ')
        super().save(*args, **kwargs)

class DoctorsQualification(models.Model):
    name = models.ForeignKey(doctors, on_delete=models.CASCADE, related_name="doctorsQualification", null=True, blank=True)
    image = models.ImageField(upload_to='stomat/image/', null=True, blank=True)

class service(models.Model):
    name = models.CharField(max_length=250)
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE , related_name="service")

    class Meta: 
        ordering = ['name']
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.name


class ourJobs(models.Model):
    image = models.ImageField()
    description = models.TextField()

class Price(models.Model):
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE , related_name="price")

    class Meta: 
        ordering = ['name']
        verbose_name = "Услуга(цена)"
        verbose_name_plural = "Услуги(цена)"

    def __str__(self):
        return self.name


# class order(models.Model):



