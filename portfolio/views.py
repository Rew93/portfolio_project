from django.shortcuts import render

from blog.models import CategoryModel, BlogModel, CommentsModel
from portfolio.models import PortfolioModel

# Create your views here.
popular_blog = sorted(BlogModel.objects.all(), key=lambda x: x.count_comment, reverse=True)
recent_comments = sorted(CommentsModel.objects.filter(parent=None), key=lambda x: len(x.children), reverse=True)
categories = CategoryModel.objects.all()

def portfolios(request, category_slug=None):
    portfolios_all = PortfolioModel.objects.all().order_by(
        '-date_create') if category_slug is None else PortfolioModel.objects.filter(category=category_slug).order_by(
        '-date_create')
    context = {
        'portfolios': portfolios_all,
        'categories': categories,
        'popular_blog': popular_blog[:5],
        'popular_blog_2': popular_blog[:2],
        'recent_comments': recent_comments[:5],

    }
    return render(request, 'portfolio/portfolios.html', context)


def portfolio(request, portfolio_id):
    portfolio = PortfolioModel.objects.get(id=portfolio_id)
    id_category = list(portfolio.category.values_list('id', flat=True))
    # id_category = [i.id for i in portfolio.category.all()]
    portfolio_category = PortfolioModel.objects.filter(category__in=id_category)
    context = {
        'portfolio': portfolio,
        'related_projects': portfolio_category,
        'categories': categories,
        'popular_blog': popular_blog[:5],
        'popular_blog_2': popular_blog[:2],
        'recent_comments': recent_comments[:5],
    }
    return render(request, 'portfolio/portfolio.html', context)
