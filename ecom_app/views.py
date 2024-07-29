from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from .models import CustomUser, Profile
from django.contrib.auth.models import Permission
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Product
from .forms import ProductForm


def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def shop(request):
    return render(request, 'shop.html')

def blog(request):
    return render(request, 'blog.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if CustomUser.objects.filter(username=username).exists():
                return render(request, 'register.html', {'error': 'Username already taken'})
            elif CustomUser.objects.filter(email=email).exists():
                return render(request, 'register.html', {'error': 'Email already taken'})
            else:
                user = CustomUser.objects.create_user(username=username, email=email, password=password1)
                user.save()
                Profile.objects.create(user=user, user_type='customer')
                return redirect('login')
        else:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
    return render(request, 'register.html')

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                profile = Profile.objects.get(user=user)
                if profile.user_type == 'admin':
                    return redirect('list_users')  # Redirect to admin page if user is admin
                elif profile.user_type == 'manager':
                    return redirect('product_list')  # Redirect to manager page if user is manager
                else:
                    return redirect('home')  # Redirect to user home page if not admin or manager
            except Profile.DoesNotExist:
                return render(request, 'index.html', {'error': 'Profile not found'})
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')



CustomUser = get_user_model()

def create_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        bio = request.POST['bio']
        location = request.POST['location']
        # birth_date = request.POST['birth_date']
        user_type = request.POST['user_type']
        permission_ids = request.POST.getlist('permissions')
        
        user = CustomUser.objects.create_user(username=username, email=email, password=password, user_type=user_type)
        Profile.objects.create(user=user, bio=bio, location=location)
        
        if permission_ids:
            permissions = Permission.objects.filter(id__in=permission_ids)
            user.user_permissions.set(permissions)
        
        user.save()
        messages.success(request, 'User created successfully.')
        return redirect('list_users')
    else:
        permissions = Permission.objects.all()
        return render(request, 'create_user.html', {'permissions': permissions})

CustomUser = get_user_model()

@login_required
def list_users(request):
    users = CustomUser.objects.all()
    user_profiles = {profile.user.id: profile for profile in Profile.objects.all()}
    
    context = {
        'users': users,
        'user_profiles': user_profiles,
    }
    return render(request, 'list_users.html', context)


def update_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.save()
        profile.bio = request.POST.get('bio', profile.bio)
        profile.location = request.POST.get('location', profile.location)
        # profile.birth_date = request.POST.get('birth_date', profile.birth_date)
        profile.user_type = request.POST.get('user_type', profile.user_type)
        profile.selected_permissions.set(request.POST.getlist('permissions'))
        permissions = request.POST.getlist('permissions')
        profile.selected_permissions.set(Permission.objects.filter(id__in=permissions))
        profile.save()
        profile.save()
        return redirect('list_users')

    permissions = Permission.objects.all()
    return render(request, 'update_user.html', {'user': user, 'permissions': permissions})


def delete_user(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        user.delete()
        return redirect('list_users')
    except CustomUser.DoesNotExist:
        return redirect('list_users')



@login_required
def admin_only_view(request):
    try:
        profile = Profile.objects.get(user=request.user)
        if profile.user_type != 'admin':
            return render(request, 'list_users.html')  # Render the admin-only page
        elif profile.user_type == 'manager':
            return redirect('manager_page')  # Redirect to manager page if user is a manager
        else:
            return redirect('unauthorized')  # Render the admin-only page
    except Profile.DoesNotExist:
        return redirect('unauthorized')  # Redirect if profile does not exist

def unauthorized_view(request):
    return render(request, 'unauthorized.html')

@login_required
def manager_only_view(request):
    try:
        profile = Profile.objects.get(user=request.user)
        if profile.user_type == 'manager':
            return render(request, 'manager_page.html')  # Render the manager-only page
        else:
            return redirect('unauthorized')  # Redirect to an unauthorized access page
    except Profile.DoesNotExist:
        return redirect('unauthorized') 
    
    from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order

def shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})

@login_required
def order_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        total_price = quantity * product.price
        Order.objects.create(user=request.user, product=product, quantity=quantity, total_price=total_price)
        return redirect('order_success')

    return render(request, 'order_product.html', {'product': product})

@login_required
def order_success(request):
    return render(request, 'order_success.html')

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'my_orders.html', {'orders': orders})



@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Replace with your product list URL
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # or any other appropriate view
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form, 'product': product})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')  # Replace with your product list URL
    return render(request, 'product_confirm_delete.html', {'product': product})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})
