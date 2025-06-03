from django.urls import path
from . import views

app_name = 'templates_store'

urlpatterns = [
    # Template listing and detail views
    path('', views.template_list, name='template_list'),
    path('category/<slug:category_slug>/', views.template_list, name='template_list_by_category'),
    path('type/<str:template_type>/', views.template_list, name='template_list_by_type'),
    path('template/<slug:template_slug>/', views.template_detail, name='template_detail'),
    
    # Template management (for sellers)
    path('template/create/', views.create_template, name='create_template'),
    path('template/<slug:template_slug>/edit/', views.edit_template, name='edit_template'),
    path('template/<slug:template_slug>/delete/', views.delete_template, name='delete_template'),
    
    # Purchase and download
    path('template/<slug:template_slug>/purchase/', views.purchase_template, name='purchase_template'),
    path('template/<slug:template_slug>/download/', views.download_template, name='download_template'),
    
    # Search and filtering
    path('search/', views.search_templates, name='search_templates'),
    path('filter/', views.filter_templates, name='filter_templates'),
    
    # Categories
    path('categories/', views.category_list, name='category_list'),
    
    # Reviews and ratings
    path('template/<slug:template_slug>/review/', views.add_review, name='add_review'),
    path('template/<slug:template_slug>/reviews/', views.template_reviews, name='template_reviews'),
]
