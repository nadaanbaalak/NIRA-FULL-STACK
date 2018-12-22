from django.contrib import admin
from django.urls import path,include
from .views import customer,admin,home

urlpatterns = [
    path('accounts/',include('django.contrib.auth.urls')),
    path('accounts/signup',customer.CustomerSignUpView.as_view(),name='customer_signup'),
    path('customer/home',customer.TicketListView.as_view(),name = 'customer_home'),

    path('customer/create_ticket',customer.TicketCreateView.as_view(),name='create_ticket'),
    path('admin/home',admin.AdminTicketListView.as_view(),name = 'admin_home'),
    path('accounts/login_success',home.login_success,name='login_success'),
    path('customer/tickets/<int:pk>', customer.TicketDetailView.as_view(), name='ticket_detail'),
    path('customer/tickets/add_reply',customer.CommentCreateView.as_view(),name = 'add_reply'),
    path('admin/tickets/<int:pk>', admin.AdminTicketDetailView.as_view(), name='admin_ticket_detail'),
    path('admin/tickets/<int:pk>/update', admin.AdminTicketUpdateView, name='admin_ticket_update'),
]