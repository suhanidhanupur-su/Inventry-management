from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm, RegisterForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse


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
            fail_silently=True,
        )

        login(request, user)
        return redirect('product_list')

    return render(request, 'register.html', {'form': form})


from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse


def send_test_email(request):
    """Send a test email using the SMTP credentials configured in settings."""
    
    subject = 'Inventory Management Test Email'
    message = 'This is a test email sent from Django using the configured SMTP settings.'
    
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [settings.EMAIL_RECEIPT_ADDRESS]

    try:
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False
        )

        return HttpResponse(
            f'Test email sent successfully to {settings.EMAIL_RECEIPT_ADDRESS}'
        )

    except Exception as exc:
        return HttpResponse(
            f'Error sending test email: {exc}',
            status=500
        )