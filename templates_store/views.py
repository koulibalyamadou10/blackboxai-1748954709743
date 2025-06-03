from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import FileResponse
from .models import Template, Category, Purchase
import uuid

def template_list(request, category_slug=None, template_type=None):
    templates = Template.objects.filter(is_active=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        templates = templates.filter(category=category)
    
    if template_type:
        templates = templates.filter(template_type=template_type)
        
    # Search functionality
    query = request.GET.get('q')
    if query:
        templates = templates.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    
    # Sorting
    sort = request.GET.get('sort')
    if sort == 'price_low':
        templates = templates.order_by('price')
    elif sort == 'price_high':
        templates = templates.order_by('-price')
    elif sort == 'newest':
        templates = templates.order_by('-created_at')
    else:
        templates = templates.order_by('-created_at')
    
    categories = Category.objects.all()
    
    context = {
        'templates': templates,
        'categories': categories,
        'current_category': category_slug,
        'current_type': template_type,
        'search_query': query,
        'sort': sort
    }
    
    return render(request, 'templates_store/template_list.html', context)

def template_detail(request, template_slug):
    template = get_object_or_404(Template, slug=template_slug, is_active=True)
    has_purchased = False
    
    if request.user.is_authenticated:
        has_purchased = Purchase.objects.filter(user=request.user, template=template).exists()
    
    context = {
        'template': template,
        'has_purchased': has_purchased
    }
    
    return render(request, 'templates_store/template_detail.html', context)

@login_required
def create_template(request):
    if not hasattr(request.user, 'sellerprofile'):
        return redirect('accounts:become_seller')
        
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        template_type = request.POST.get('template_type')
        price = request.POST.get('price')
        
        if not all([title, description, category_id, template_type, price]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('templates_store:create_template')
            
        try:
            template = Template.objects.create(
                title=title,
                description=description,
                category_id=category_id,
                template_type=template_type,
                price=price,
                author=request.user
            )
            
            if 'preview_image' in request.FILES:
                template.preview_image = request.FILES['preview_image']
            if 'file' in request.FILES:
                template.file = request.FILES['file']
                
            template.save()
            messages.success(request, 'Template created successfully!')
            return redirect('templates_store:template_detail', template_slug=template.slug)
            
        except Exception as e:
            messages.error(request, f'Error creating template: {str(e)}')
            return redirect('templates_store:create_template')
    
    categories = Category.objects.all()
    return render(request, 'templates_store/create_template.html', {'categories': categories})

@login_required
def edit_template(request, template_slug):
    template = get_object_or_404(Template, slug=template_slug, author=request.user)
    
    if request.method == 'POST':
        template.title = request.POST.get('title', template.title)
        template.description = request.POST.get('description', template.description)
        template.category_id = request.POST.get('category', template.category_id)
        template.template_type = request.POST.get('template_type', template.template_type)
        template.price = request.POST.get('price', template.price)
        
        if 'preview_image' in request.FILES:
            template.preview_image = request.FILES['preview_image']
        if 'file' in request.FILES:
            template.file = request.FILES['file']
            
        template.save()
        messages.success(request, 'Template updated successfully!')
        return redirect('templates_store:template_detail', template_slug=template.slug)
    
    categories = Category.objects.all()
    return render(request, 'templates_store/edit_template.html', {
        'template': template,
        'categories': categories
    })

@login_required
def delete_template(request, template_slug):
    template = get_object_or_404(Template, slug=template_slug, author=request.user)
    
    if request.method == 'POST':
        template.delete()
        messages.success(request, 'Template deleted successfully!')
        return redirect('accounts:user_templates')
    
    return render(request, 'templates_store/delete_template.html', {'template': template})

@login_required
def purchase_template(request, template_slug):
    template = get_object_or_404(Template, slug=template_slug, is_active=True)
    
    # Check if already purchased
    if Purchase.objects.filter(user=request.user, template=template).exists():
        messages.error(request, 'You have already purchased this template.')
        return redirect('templates_store:template_detail', template_slug=template.slug)
    
    # TODO: Implement actual payment processing here
    # For now, create a purchase record directly
    Purchase.objects.create(
        user=request.user,
        template=template,
        transaction_id=str(uuid.uuid4()),
        amount=template.price
    )
    
    messages.success(request, 'Template purchased successfully!')
    return redirect('templates_store:download_template', template_slug=template.slug)

@login_required
def download_template(request, template_slug):
    template = get_object_or_404(Template, slug=template_slug)
    
    # Verify purchase
    if not Purchase.objects.filter(user=request.user, template=template).exists():
        messages.error(request, 'You must purchase this template before downloading.')
        return redirect('templates_store:template_detail', template_slug=template.slug)
    
    try:
        return FileResponse(template.file, as_attachment=True)
    except Exception as e:
        messages.error(request, f'Error downloading template: {str(e)}')
        return redirect('templates_store:template_detail', template_slug=template.slug)

def search_templates(request):
    query = request.GET.get('q', '')
    templates = Template.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query)
    ).filter(is_active=True)
    
    return render(request, 'templates_store/search_results.html', {
        'templates': templates,
        'query': query
    })

def filter_templates(request):
    templates = Template.objects.filter(is_active=True)
    
    # Apply filters
    category = request.GET.get('category')
    if category:
        templates = templates.filter(category__slug=category)
    
    template_type = request.GET.get('type')
    if template_type:
        templates = templates.filter(template_type=template_type)
    
    min_price = request.GET.get('min_price')
    if min_price:
        templates = templates.filter(price__gte=min_price)
    
    max_price = request.GET.get('max_price')
    if max_price:
        templates = templates.filter(price__lte=max_price)
    
    sort = request.GET.get('sort')
    if sort == 'price_low':
        templates = templates.order_by('price')
    elif sort == 'price_high':
        templates = templates.order_by('-price')
    elif sort == 'newest':
        templates = templates.order_by('-created_at')
    
    return render(request, 'templates_store/template_list.html', {
        'templates': templates,
        'categories': Category.objects.all()
    })

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'templates_store/category_list.html', {'categories': categories})

@login_required
def add_review(request, template_slug):
    template = get_object_or_404(Template, slug=template_slug)
    
    # Verify purchase
    if not Purchase.objects.filter(user=request.user, template=template).exists():
        messages.error(request, 'You must purchase this template before reviewing.')
        return redirect('templates_store:template_detail', template_slug=template.slug)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if rating and comment:
            # TODO: Implement review model and creation
            messages.success(request, 'Review added successfully!')
        else:
            messages.error(request, 'Please provide both rating and comment.')
            
    return redirect('templates_store:template_detail', template_slug=template.slug)

def template_reviews(request, template_slug):
    template = get_object_or_404(Template, slug=template_slug)
    # TODO: Implement review listing
    return render(request, 'templates_store/template_reviews.html', {'template': template})
