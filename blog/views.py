from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import HttpResponseRedirect, render, reverse
from django.utils.text import slugify

from blog.decorators import verify_author, verify_author_comment
from blog.forms import BlogForm, CommentsForm, UpdateBlogForm
from blog.models import BlogModel, CategoryModel, CommentsModel

# Create your views here.
popular_blog = sorted(BlogModel.objects.all(), key=lambda x: x.count_comment, reverse=True)
category = CategoryModel.objects.all()
recent_comments = sorted(CommentsModel.objects.filter(parent=None), key=lambda x: len(x.children), reverse=True)


def custom_404_page(request, exception):
    return render(request, 'blog/404.html', status=404)


def blogs(request, page_number=1, category_id=None, author_id=None):
    if category_id:
        blogs = BlogModel.objects.filter(category=category_id).order_by('-date_create', 'title')
    elif author_id:
        blogs = BlogModel.objects.filter(author=author_id).order_by('-date_create', 'title')
    else:
        blogs = BlogModel.objects.all()

    paginator = Paginator(blogs, 4)
    blogs_paginator = paginator.page(page_number)
    context = {
        'length': len(blogs),
        'categories': category,
        'blogs': blogs_paginator,
        'popular_blog': popular_blog[:5],
        'popular_blog_2': popular_blog[:2],
        'recent_comments': recent_comments[:5],
    }
    return render(request, 'blog/blogs.html', context)


def blog(request, slug, page_number=1):
    blog = BlogModel.objects.get(slug=slug)
    comments = CommentsModel.objects.filter(blog=blog.id)
    paginator = Paginator(comments, 6)
    comments_paginator = paginator.page(page_number)

    if request.method == 'POST':
        form = CommentsForm(data=request.POST)
        if form.is_valid():
            comment_form = form.save(commit=False)
            comment_form.blog = blog
            comment_form.author = request.user
            comment_form.save()
            return HttpResponseRedirect(reverse('blog', args=[slug]))
    else:
        form = CommentsForm()
    context = {
        'categories': category,
        'blog': blog,
        'form': form,
        'popular_blog': popular_blog[:5],
        'popular_blog_2': popular_blog[:2],
        'comments': comments_paginator,
        'recent_comments': recent_comments[:5],
    }
    return render(request, 'blog/blog.html', context)


def search(request, page_number=1):
    result = []
    if request.method == 'GET':
        query = request.GET.get('q')
        if query == '':
            query = 'None'

        result = BlogModel.objects.filter(
            Q(title__icontains=query) | Q(text_story__icontains=query) | Q(author__icontains=query))
    paginator = Paginator(result, 4)
    paginator_page = paginator.page(page_number)
    return render(request, 'blog/search.html', {
        'length': len(result),
        'results': paginator_page,
        'popular_blog': popular_blog[:5],
        'popular_blog_2': popular_blog[:2],
        'categories': category,
    })


@login_required(login_url='login_register')
def reply_page(request):
    if request.method == 'POST':
        form = CommentsForm(data=request.POST)
        blog_id = request.POST.get('blog_id')
        comment_id = request.POST.get('parent')
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.blog = BlogModel(id=blog_id)
            reply.parent = CommentsModel(id=comment_id)
            reply.save()
            messages.success(request, 'Your comment was add.')
            return HttpResponseRedirect(reverse('blog', args=[BlogModel.objects.get(id=blog_id).slug]))
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)


@verify_author_comment
def comment_del(request, comment_id):
    comment = CommentsModel.objects.get(id=comment_id)
    slug_blog = comment.blog.slug
    comment.delete()
    messages.success(request, 'Your comment was delete.')
    return HttpResponseRedirect(reverse('blog', args=[slug_blog]))


@verify_author_comment
def comment_update(request, comment_id):
    comment = CommentsModel.objects.filter(id=comment_id).first()
    if request.method == 'POST':
        form = CommentsForm(data=request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your comment was edit.')
            return HttpResponseRedirect(reverse('blog', args=[comment.blog.slug]))
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = CommentsForm(instance=comment)
    context = {
        'categories': category,
        'popular_blog': popular_blog[:5],
        'popular_blog_2': popular_blog[:2],
        'recent_comments': recent_comments[:5],
        'form': form,
        'comment': comment,
    }
    return render(request, 'blog/update_comment.html', context)


@login_required(login_url='login_register')
def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            text_story = form.cleaned_data['text_story']
            slug = slugify(form.cleaned_data['title'])
            author = request.user
            image = form.cleaned_data['image']
            image_2 = form.cleaned_data['image_2']
            video = form.cleaned_data['video']
            obj = BlogModel(title=title, text_story=text_story, slug=slug, author=author, image=image, image_2=image_2,
                            video=video)
            obj.save()
            form2 = BlogForm(request.POST, instance=obj)
            form2.save(commit=False)
            form2.save_m2m()
            messages.success(request, f'You successful add blog: "{title}".')
            return HttpResponseRedirect(reverse('blogs'))
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = BlogForm()
    context = {
        'form': form,
        'categories': category,
        'popular_blog': popular_blog[:5],
        'popular_blog_2': popular_blog[:2],
        'recent_comments': recent_comments[:5],
    }
    return render(request, 'blog/add_new_blog.html', context)


@verify_author
def update_blog(request, slug):
    blog = BlogModel.objects.filter(slug=slug).first()
    if request.method == 'POST':
        form = UpdateBlogForm(data=request.POST, instance=blog, files=request.FILES)
        clear_image = request.POST.get('image-clear')
        clear_image_2 = request.POST.get('image_2-clear')
        clear_video = request.POST.get('video-clear')
        if form.is_valid():
            if clear_image:
                blog.image.delete()
            if clear_image_2:
                blog.image_2.delete()
            if clear_video:
                blog.video.delete()
            form.save()
            messages.success(request, f'Your blog {blog.title} is updated.')
            return HttpResponseRedirect(reverse('blog', args=[blog.slug]))
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = UpdateBlogForm(instance=blog)
    context = {
        'form': form,
        'categories': category,
        'popular_blog': popular_blog[:5],
        'popular_blog_2': popular_blog[:2],
        'recent_comments': recent_comments[:5],
        'blog': blog,
    }
    return render(request, 'blog/update_new_blog.html', context)


@verify_author
def del_blog(request, slug):
    blog = BlogModel.objects.get(slug=slug)
    messages.success(request, f'Your blog {blog.title} is delete.')
    blog.delete()
    return HttpResponseRedirect(reverse('blogs'))
