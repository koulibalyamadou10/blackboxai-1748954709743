from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/seller/', views.seller_profile, name='seller_profile'),
    path('profile/seller/edit/', views.edit_seller_profile, name='edit_seller_profile'),
    path('profile/purchases/', views.purchase_history, name='purchase_history'),
    path('profile/sales/', views.sales_history, name='sales_history'),
    path('profile/templates/', views.user_templates, name='user_templates'),
    path('profile/become-seller/', views.become_seller, name='become_seller'),
]
