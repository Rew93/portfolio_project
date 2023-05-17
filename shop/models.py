from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from blog.models import CommentsModel, CategoryModel


# Create your models here.
class BrandModel(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'brand'
        verbose_name_plural = 'brands'

    def __str__(self):
        return f'{self.name}'


class CategoryProductModel(CategoryModel):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Categorie'


class ImagesModel(models.Model):
    describe_image = models.CharField(max_length=100)
    image_1 = models.ImageField(upload_to='shop/product/image', null=True, blank=True)
    image_2 = models.ImageField(upload_to='shop/product/image', null=True, blank=True)
    image_3 = models.ImageField(upload_to='shop/product/image', null=True, blank=True)
    image_4 = models.ImageField(upload_to='shop/product/image', null=True, blank=True)

    def __str__(self):
        return f'{self.describe_image}'
    class Meta:
        verbose_name = 'Image'


class SizeGridModel(models.Model):
    name = models.CharField(max_length=5)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('name',)
        verbose_name = 'Grid size'


class ProductModel(models.Model):
    GENDER_CHOICE = [
        ("M", "Male"),
        ("F", "Female"),
    ]
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=8, decimal_places=2)  # max 999999,99
    category = models.ManyToManyField(CategoryProductModel)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    compositions = models.CharField(max_length=150)
    color = models.CharField(max_length=30)
    brand = models.ForeignKey(BrandModel, on_delete=models.CASCADE)
    images = models.OneToOneField(ImagesModel, on_delete=models.CASCADE)
    sizes = models.ManyToManyField(SizeGridModel)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return f'{self.name}'


class ProductSizeModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    size = models.ForeignKey(SizeGridModel, on_delete=models.CASCADE)
    count = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'{self.product} this size:{self.size} = {self.count}'

    class Meta:
        verbose_name = 'Product size & count'


class ReviewModel(CommentsModel):
    rating = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1),
                                                                     MaxValueValidator(5)])
    product = models.ForeignKey(ProductModel, on_delete=models.PROTECT)
    parent_review = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    @property
    def children(self):
        return ReviewModel.objects.filter(parent_review=self).reverse()

    @property
    def is_parent(self):
        if self.parent_review is None:
            return True
        return False

    class Meta:
        verbose_name = 'Review'
