from django.db import models

from users.models import UserModel
from blog.models import CategoryModel


# Create your models here.
class PortfolioModel(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    description = models.TextField(max_length=1500)
    development = models.CharField(max_length=200)
    design = models.CharField(max_length=200)
    photography = models.CharField(max_length=200)
    image = models.ImageField(upload_to='portfolio/image', null=True, blank=True)
    image_2 = models.ImageField(upload_to='portfolio/image', null=True, blank=True)
    image_3 = models.ImageField(upload_to='portfolio/image', null=True, blank=True)
    video = models.FileField(upload_to='portfolio/video', null=True, blank=True)
    client = models.CharField(max_length=150)
    date_create = models.DateField()
    link_on_project = models.URLField(max_length=128, unique=True, blank=True, null=True, default='https//:')
    category = models.ManyToManyField(CategoryModel)

    class Meta:
        verbose_name = 'Portfolio'
        verbose_name_plural = 'Portfolios'

