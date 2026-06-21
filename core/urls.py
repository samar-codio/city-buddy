from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.ManualLoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('order/', views.place_order, name='place_order'),
    path('payment/<int:order_id>/', views.submit_payment, name='submit_payment'),
    path('price-list/', views.price_list_view, name='price_list'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]
