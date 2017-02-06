from django.shortcuts import render
from django.http import HttpResponse
from Rango.models import Category
from Rango.models import Page
from Rango.forms import CategoryForm
from Rango.forms import PageForm, UserForm, UserProfileForm

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

def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request,'Rango/add_category.html', {'form':form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'Rango/add_page.html', context_dict)

def register(request):
# A boolean value for telling the template
# whether the registration was successful.
# Set to False initially. Code changes value to
# True when registration succeeds.
    registered = False
# If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
# Attempt to grab information from the raw form information.
# Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
# If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
# Save the user's form data to the database.
            user = user_form.save()
# Now we hash the password with the set_password method.
# Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()
# Now sort out the UserProfile instance.
# Since we need to set the user attribute ourselves,
# we set commit=False. This delays saving the model
# until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
# Did the user provide a profile picture?
# If so, we need to get it from the input form and
#put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
# Now we save the UserProfile model instance.
            profile.save()
# Update our variable to indicate that the template
# registration was successful.
            registered = True
        else:
# Invalid form or forms - mistakes or something else?
# Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
# Not a HTTP POST, so we render our form using two ModelForm instances.
# These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()
# Render the template depending on the context.
    return render(request,'Rango/register.html',{'user_form': user_form,'profile_form': profile_form,'registered': registered})