from django.db import models
from django.utils import timezone

from users.models import UserModel


# Create your models here.
class CategoryModel(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.slug}'

    @property
    def category_count(self):
        return BlogModel.objects.filter(category=self).count()


class BlogModel(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True)
    text_story = models.TextField()
    image = models.ImageField(upload_to='blog/images/', null=True, blank=True)
    image_2 = models.ImageField(upload_to='blog/images/', null=True, blank=True)
    image_popular_blog = models.ImageField(upload_to='blog/images/', null=True, blank=True)
    video = models.FileField(upload_to='blog/video/', null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(CategoryModel)

    def __str__(self):
        return f'{self.title}'

    def short_text(self):
        return self.text_story[:500]

    @property
    def count_comment(self):
        return CommentsModel.objects.filter(blog=self, parent=None).count()

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'


class CommentsModel(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    text_comment = models.TextField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(BlogModel, on_delete=models.PROTECT, related_name='blog')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f'Comment {self.author} to blog {self.blog.title}'

    class Meta:
        ordering = ['-date_created']

    @property
    def children(self):
        return CommentsModel.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
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
