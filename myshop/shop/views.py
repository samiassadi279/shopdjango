from django.shortcuts import render,redirect,get_object_or_404
from .models import Category, Product,Type
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import  SignUp
from django.http import HttpResponse
from django.contrib.auth.models import User
#from cart.forms import CartAddProductForm
def product_list(request, category_slug, type_slug=None):
    product_type=None
    category = get_object_or_404(Category, slug=category_slug)
    types = Type.objects.filter(category=category)
    if request.GET.get('price_filter')=='3':
        products = Product.objects.filter(available=True, category=category).order_by('-price')
    elif request.GET.get('price_filter')=='2':
        products = Product.objects.filter(available=True, category=category).order_by('price')
    else:
        products = Product.objects.filter(available=True,category=category)
    if type_slug:
        product_type = get_object_or_404(Type, slug=type_slug)
        products.filter(product_type=product_type)
    return render(request, 'category.html', {'category': category,
                                                      'types': types,
                                                      'products': products,
                                                      'product_type':product_type,
                                                      })
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    #cart_product_form = CartAddProductForm()
    return render(request, 'detail.html', {'product': product,
                                                        #'cart_product_form': cart_product_form
                                                        })
def home(request):
    categories = Category.objects.all()
    return render(request, template_name='homepage.html',context= {'categories': categories} )

def register(request):
    if request.method == "POST":
        form = SignUp(data=request.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                messages.error(request, f"Account associated with this email already exists, Login instead")
                return render(request = request,
                          template_name = "register.html",
                          context={"form":form})
            else:
                user = form.save()
                username = form.cleaned_data.get('username')
                login(request, user)
                messages.success(request, f"New account created: {username}")
                return redirect("/")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "register.html",
                          context={"form":form})
   
    form = SignUp
    return render(request = request,
                template_name = "register.html",
                context={"form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/")

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "login.html",
                    context={"form":form})

