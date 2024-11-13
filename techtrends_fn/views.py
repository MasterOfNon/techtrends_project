from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category  #importing models for accessing db
from django.contrib.auth.decorators import login_required

@login_required(login_url='login/')
def home(request):
    products = Product.objects.select_related('category').all() #This line is used in Django to fetch product data, along with related category data 
    categories= Category.objects.all()# getb all categories : phone, laptop and wearables
    context={
        'products': products,
        'categories': categories,
        'range_5': range(5),
    }
    return render(request, 'home.html', context)

@login_required(login_url='login/')
def category_selected(request, category_slug):
    category= get_object_or_404(Category,slug=category_slug) # gets the name of the category belonging to the slug of the prodcut the user selected.
    products= Product.objects.filter(category=category) #matches with the category column of the Products table.
    context={
        'products': products,
        'selected_category':category,
    }
    return render(request, 'category_selected.html', context)


@login_required(login_url='login/')
def search_products(request):
    query=request.GET.get('q')
    products=Product.objects.all()
    if query:
        products=products.filter(name__icontains=query)

    return render (request, 'Search_result.html',{'products':products, 'query':query})







