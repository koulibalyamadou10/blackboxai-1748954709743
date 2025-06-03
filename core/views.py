from django.shortcuts import render
from django.contrib import messages
from .models import FAQ, ContactMessage, SiteConfiguration
from templates_store.models import Template, Category

def home(request):
    # Get featured templates
    featured_templates = Template.objects.filter(is_active=True).order_by('-created_at')[:6]
    
    # Get all categories
    categories = Category.objects.all()
    
    # Get site configuration
    site_config = SiteConfiguration.objects.first()
    
    context = {
        'featured_templates': featured_templates,
        'categories': categories,
        'site_config': site_config,
    }
    return render(request, 'core/home.html', context)

def about(request):
    site_config = SiteConfiguration.objects.first()
    return render(request, 'core/about.html', {'site_config': site_config})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if name and email and subject and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            messages.success(request, 'Your message has been sent successfully!')
        else:
            messages.error(request, 'Please fill in all fields.')
            
    return render(request, 'core/contact.html')

def faq(request):
    faqs = FAQ.objects.filter(is_active=True).order_by('order')
    return render(request, 'core/faq.html', {'faqs': faqs})

def terms(request):
    return render(request, 'core/terms.html')

def privacy(request):
    return render(request, 'core/privacy.html')

def handler404(request, exception):
    return render(request, 'core/404.html', status=404)

def handler500(request):
    return render(request, 'core/500.html', status=500)
