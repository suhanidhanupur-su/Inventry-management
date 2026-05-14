from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm, RegisterForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings


# Product List
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


# Add Product
@login_required
def add_product(request):
    form = ProductForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('product_list')

    return render(request, 'product_form.html', {'form': form})


# Edit Product
@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    form = ProductForm(request.POST or None, request.FILES or None, instance=product)

    if form.is_valid():
        form.save()
        return redirect('product_list')

    return render(request, 'product_form.html', {'form': form})


# Delete Product
@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('product_list')

    return render(request, 'delete.html', {'product': product})


# Register
def register(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save()

        # Welcome Email
        send_mail(
            'Welcome to Inventory Management',
            'Your account has been created successfully.',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        login(request, user)
        return redirect('product_list')

    return render(request, 'register.html', {'form': form})