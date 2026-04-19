from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('order/', views.place_order, name='place_order'),
    path('payment/<int:order_id>/', views.submit_payment, name='submit_payment'),
]