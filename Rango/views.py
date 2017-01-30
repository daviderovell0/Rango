from django.shortcuts import render
from django.http import HttpResponse
from Rango.models import Category
from Rango.models import Page

def about(request):
    return render(request,"Rango/about.html")

def show_category(request, categoryNameSlug):
    context_dict = {}
    try:
        category= Category.objects.get(slug = categoryNameSlug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'Rango/category.html', context_dict)

def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    category_list = Category.objects.order_by('-likes')[:5]
    pagesList = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': pagesList}
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'Rango/index.html', context=context_dict)