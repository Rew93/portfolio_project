from allauth.account.models import EmailAddress
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


# Create your models here.
class UserModel(AbstractUser):
    redex_phone = RegexValidator(
        regex=r'^\+?3?8?0\d{2}-? ?\d{3}-? ?\d{2}-? ?\d{2}$',
        message="Phone number must be entered in the format: '+380999999999'. Up to 12 digits allowed.")
    phone_number = models.CharField(validators=[redex_phone], blank=True, null=True, max_length=16)
    image = models.ImageField(upload_to='users/image/', blank=True, null=True)
    is_verified = models.CharField(default=False)

    # @property
    # def verified_email(self):
    #     list_email = [i.email for i in EmailAddress.objects.all()]
    #     if self.email in list_email:
    #         self.is_verified = True
    #         self.save()
    #         return self

    class Meta:
        ordering = ['last_name']
        verbose_name = 'User'
        verbose_name_plural = 'User'

    def __str__(self):
        return self.get_full_name()
