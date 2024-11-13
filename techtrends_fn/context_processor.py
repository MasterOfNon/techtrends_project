from .models import Category
# this file is created so that categroy can be accesed by every template without rendering in view.
#to use this register in setting.py templates

def categories_processor(request):
    categories= Category.objects.all()
    return {'categories' : categories }

def Range5(request):

    return {'range_5':range(5)}