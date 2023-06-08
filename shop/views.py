from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404

from blog.models import BlogModel, CommentsModel, CategoryModel
from shop.decorators import verify_author_review
from shop.forms import ReviewForm, ReplyReviewForm, EditReviewForm
from shop.models import ProductModel, ReviewModel, CheckoutModel, CouponCodeModel, BrandModel, CategoryProductModel

# Create your views here.
popular_blog = sorted(BlogModel.objects.all(), key=lambda x: x.count_comment, reverse=True)
recent_comments = sorted(CommentsModel.objects.filter(parent=None), key=lambda x: len(x.children), reverse=True)
categories = CategoryModel.objects.all()


def products(request, page_number=1):
    products_all = ProductModel.objects.all()
    brands = BrandModel.objects.all()
    categories_product_parent = CategoryProductModel.objects.filter(parent=None)
    categories_product_children = CategoryProductModel.objects.filter(parent__isnull=False)
    if request.method == 'POST':
        category_parent = request.POST.get('category_parent')
        gender = request.POST.get('gender')
        category_children = request.POST.get('category_children')
        if category_parent != 'all':
            products_all = products_all.filter(category__slug=category_parent)
        if gender != 'all':
            products_all = products_all.filter(gender=gender)
        if category_children != 'all':
            products_all = products_all.filter(category__slug=category_children)
    paginator = Paginator(products_all, 4)
    products_paginator = paginator.page(page_number)
    context = {
        'length': len(products_all),
        'brands': brands,
        'categories_product_parent': categories_product_parent,
        'categories_product_children': categories_product_children,
        'products': products_paginator,
        'categories': categories,
        'popular_blog': popular_blog[:5],
        'popular_blog_2': popular_blog[:2],
        'recent_comments': recent_comments[:5],
    }
    return render(request, 'shop/products.html', context)


def product(request, slug_product, id=None):
    product_one = get_object_or_404(ProductModel, slug=slug_product)
    name_category = list(product_one.category.values_list('name', flat=True))
    reviews = ReviewModel.objects.filter(product=product_one, parent_review=None).order_by('date_created')
    review = get_object_or_404(ReviewModel, id=id) if id else None
    if request.method == 'GET':
        context = {
            'reviews': reviews,
            'add_form': ReviewForm(),
            'reply_form': ReplyReviewForm(),
            'edit_form': EditReviewForm(instance=review),
            'product_categories': name_category,
            'product': product_one,
            'categories': categories,
            'popular_blog': popular_blog[:5],
            'popular_blog_2': popular_blog[:2],
            'recent_comments': recent_comments[:5],
        }
        return render(request, 'shop/product.html', context)

    elif request.method == 'POST':
        if 'add_form' in request.POST:
            add_form = ReviewForm(data=request.POST)
            reply_form = ReplyReviewForm()
            edit_form = EditReviewForm()
            if add_form.is_valid():
                r = add_form.save(commit=False)
                r.author = request.user
                r.product = product_one
                r.save()
                messages.success(request, 'You review success added')
                return HttpResponseRedirect(reverse('product', args=[slug_product]))
            else:
                for error in list(add_form.errors.values()):
                    messages.error(request, error)
        elif 'edit_form' in request.POST:
            edit_form = EditReviewForm(instance=review, data=request.POST)
            reply_form = ReplyReviewForm()
            add_form = ReviewForm()
            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, 'You review is edited')
                return HttpResponseRedirect(reverse('product', args=[slug_product]))
            else:
                for error in list(edit_form.errors.values()):
                    messages.error(request, error)
        elif 'reply_form' in request.POST:
            reply_form = ReplyReviewForm(data=request.POST)
            product_id = request.POST.get('product_id')
            review_id = request.POST.get('parent_review')
            add_form = ReviewForm()
            edit_form = EditReviewForm()
            if reply_form.is_valid():
                reply = reply_form.save(commit=False)
                reply.product = ProductModel(id=product_id)
                reply.author = request.user
                reply.parent_review = ReviewModel(id=review_id)
                reply.save()
                messages.success(request, 'You review was added')
                return HttpResponseRedirect(
                    reverse('product', args=[slug_product]))
            else:
                for error in list(reply_form.errors.values()):
                    messages.error(request, error)
    else:
        reply_form = ReplyReviewForm()
        add_form = ReviewForm()
        edit_form = EditReviewForm()
    context = {
        'reviews': reviews,
        'add_form': add_form,
        'edit_form': edit_form,
        'reply_form': reply_form,
        'product_categories': name_category,
        'product': product_one,
        'categories': categories,
        'popular_blog': popular_blog[:5],
        'popular_blog_2': popular_blog[:2],
        'recent_comments': recent_comments[:5],
    }
    return render(request, 'shop/product.html', context)


@verify_author_review
def delete_review(request, id):
    review = ReviewModel.objects.filter(id=id).first()
    if review.children:
        review.children.delete()
    review.delete()
    messages.success(request, 'You review was deleted')
    return HttpResponseRedirect(reverse('product', args=[review.product.slug]))


@login_required(login_url='login_register')
def checkout(request):
    checkout = CheckoutModel.objects.filter(user=request.user)
    if request.method == "GET":
        code = request.GET.get('code')
        coupon_code = CouponCodeModel.objects.filter(code=code).first()
        if code:
            if coupon_code:
                if coupon_code.is_valid():
                    sum_with_discount = (checkout.total_sum() * (100 - coupon_code.discount)) / 100
                    messages.success(request, f'{coupon_code}')
                else:
                    sum_with_discount = None
                    messages.error(request, 'This coupon code is not active')
            else:
                sum_with_discount = None
                messages.error(request, 'This coupon code do not exist')
        else:
            sum_with_discount = None
    context = {
        'sum_with_discount': sum_with_discount,
        'checkouts': checkout,
    }
    return render(request, 'shop/shop_checkout.html', context)


@login_required(login_url='login_register')
def add_checkout(request, product_slug):
    product = ProductModel.objects.get(slug=product_slug)
    checkout = CheckoutModel.objects.filter(user=request.user, product=product)
    if not checkout.exists():
        CheckoutModel.objects.create(user=request.user, product=product, quantity=1)
    else:
        model = checkout.first()
        model.quantity += 1
        model.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required(login_url='login_register')
def remove_checkout(request, checkout_id):
    checkout = CheckoutModel.objects.get(id=checkout_id)
    checkout.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required(login_url='login_register')
def update_checkout(request):
    if request.method == 'GET':
        item_id = request.GET.get('item_id')
        quantity = int(request.GET.get('quantity'))

        try:
            basket_item = CheckoutModel.objects.get(id=item_id)
            basket_item.quantity = quantity
            basket_item.save()
            return JsonResponse({'success': True})
        except CheckoutModel.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Basket item not found.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
