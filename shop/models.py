from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from users.models import UserModel


# Create your models here.
class BrandModel(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'brand'
        verbose_name_plural = 'brands'

    def __str__(self):
        return f'{self.name}'


class CategoryProductModel(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=150, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

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
    name = models.CharField(max_length=5, unique=True)

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
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return f'{self.name}'

    @property
    def new_products(self):
        diff = timezone.now() - self.date_added
        return True if diff <= 2629800 else False


class ProductSizeModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    size = models.ForeignKey(SizeGridModel, on_delete=models.CASCADE)
    count = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'{self.product} this size:{self.size} = {self.count}'

    class Meta:
        verbose_name = 'Product size & count'


class ReviewModel(models.Model):
    rating = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1),
                                                                     MaxValueValidator(5)])
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    text_comment = models.TextField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(ProductModel, on_delete=models.PROTECT)
    parent_review = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    @property
    def count_review(self):
        return ReviewModel.objects.filter(parent_review=None, product=self.product).count()

    @property
    def children(self):
        return ReviewModel.objects.filter(parent_review=self).reverse()

    @property
    def is_parent(self):
        if self.parent_review is None:
            return True
        return False

    @property
    def time_ago(self):
        diff = timezone.now() - self.date_created
        if diff.seconds == 0:
            return 'now'
        elif 0 < diff.seconds < 60:
            return f'{diff.seconds} second ago'
        elif 60 <= diff.seconds < 3600:
            return f'{diff.seconds // 60} minute ago'
        elif 3600 <= diff.seconds < 86400:
            return f'{diff.seconds // 3600} hour {diff.seconds % 3600 // 60} minute ago'
        elif 1 <= diff.days < 366:
            return f'{diff.seconds // 86400} day {diff.seconds % 86400 // 3600} hour {diff.seconds % 86400 % 3600 // 60} minute ago'
        else:
            return f'{diff.deys // 366} year {diff.days % 366} day ago'

    @property
    def average_rating(self):
        r = ReviewModel.objects.filter(product=self.product, parent_review=None).values_list('rating', flat=True)
        return int(round(sum(r) / len(r), 0))

    class Meta:
        verbose_name = 'Review'


class CheckoutQuerySet(models.QuerySet):

    def total_quantity(self):
        return sum([checkout.quantity for checkout in self])

    def total_sum(self):
        return sum([checkout.sum() for checkout in self])


class CheckoutModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    objects = CheckoutQuerySet.as_manager()

    def __str__(self):
        return f'Name product: {self.product.name} | quantity: {self.quantity}'

    def sum(self):
        return self.quantity * self.product.price


class CouponCodeModel(models.Model):
    code = models.CharField(max_length=8, null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    discount = models.PositiveSmallIntegerField(default=0)
    date_expirations = models.DateTimeField()

    def is_valid(self):
        return self.date_expirations > timezone.now()

    def __str__(self):
        return f'Code: {self.code} discount: {self.discount}%'


