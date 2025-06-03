from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, SellerProfile

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('core:home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('core:home')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('accounts:register')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('accounts:register')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('accounts:register')
            
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        messages.success(request, 'Registration successful!')
        return redirect('core:home')
        
    return render(request, 'accounts/register.html')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        profile = user.profile
        
        # Update user info
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        
        # Update profile info
        profile.bio = request.POST.get('bio', profile.bio)
        profile.website = request.POST.get('website', profile.website)
        
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
            
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
        
    return render(request, 'accounts/edit_profile.html')

@login_required
def seller_profile(request):
    if not hasattr(request.user, 'sellerprofile'):
        return redirect('accounts:become_seller')
    return render(request, 'accounts/seller_profile.html')

@login_required
def edit_seller_profile(request):
    if not hasattr(request.user, 'sellerprofile'):
        return redirect('accounts:become_seller')
        
    if request.method == 'POST':
        seller_profile = request.user.sellerprofile
        seller_profile.company_name = request.POST.get('company_name', seller_profile.company_name)
        seller_profile.save()
        messages.success(request, 'Seller profile updated successfully!')
        return redirect('accounts:seller_profile')
        
    return render(request, 'accounts/edit_seller_profile.html')

@login_required
def become_seller(request):
    if hasattr(request.user, 'sellerprofile'):
        return redirect('accounts:seller_profile')
        
    if request.method == 'POST':
        SellerProfile.objects.create(
            user=request.user,
            company_name=request.POST.get('company_name', '')
        )
        request.user.profile.is_seller = True
        request.user.profile.save()
        messages.success(request, 'You are now registered as a seller!')
        return redirect('accounts:seller_profile')
        
    return render(request, 'accounts/become_seller.html')

@login_required
def purchase_history(request):
    purchases = request.user.purchases.all().order_by('-purchase_date')
    return render(request, 'accounts/purchase_history.html', {'purchases': purchases})

@login_required
def sales_history(request):
    if not hasattr(request.user, 'sellerprofile'):
        return redirect('accounts:become_seller')
        
    templates = request.user.templates.all()
    return render(request, 'accounts/sales_history.html', {'templates': templates})

@login_required
def user_templates(request):
    if not hasattr(request.user, 'sellerprofile'):
        return redirect('accounts:become_seller')
        
    templates = request.user.templates.all().order_by('-created_at')
    return render(request, 'accounts/user_templates.html', {'templates': templates})
