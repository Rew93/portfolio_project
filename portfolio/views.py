from django.shortcuts import render


# Create your views here.
def portfolios(request):
    return render(request, 'portfolio/portfolios.html')
