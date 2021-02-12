from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    FullName = models.CharField(max_length=60, null=True)
    PhoneNumber = models.CharField(max_length=15,  default='XX-XXX-XXX-XXXX')
    Address = models.CharField(max_length=30, default='DEFAULT ADDR')
    City = models.CharField(max_length=20, default='DEFAULT CITY')
    StateProvince = models.CharField(max_length=12, default='DEFAULT')
    CompanyPosition = models.CharField(max_length=30)
    Website = models.CharField(max_length=30, null=True)
    

    def __str__(self):
        return f'{self.user.username} Profile'
