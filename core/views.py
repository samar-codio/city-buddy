from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from .models import Order, PaymentProof,Banner,Offer
from .forms import PaymentProofForm
from .gsheets_utils import push_order_to_sheet, get_price_list_from_sheet


# Create your views here.
from .models import Banner, Offer

def home(request):
    banners = Banner.objects.filter(is_active=True)
    offers = Offer.objects.filter(is_active=True)
    return render(request, 'core/home.html', {
        'banners': banners,
        'offers': offers
    })

@login_required
def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            
            # 🚀 NEW: Sync to Google Sheets!
            push_order_to_sheet(order)
            
            return redirect('submit_payment', order_id=order.id)
    else:
        full_name = ""
        if hasattr(request.user, 'profile') and request.user.profile:
            full_name = request.user.profile.full_name
        else:
            full_name = request.user.get_full_name() or request.user.username
        form = OrderForm(initial={'name': full_name})
    return render(request, 'core/order_form.html', {'form': form})

# 🚀 NEW: View to show Price List from Sheets
def price_list_view(request):
    prices = get_price_list_from_sheet()
    return render(request, 'core/price_list.html', {'prices': prices})



@login_required
def submit_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Check if a payment proof already exists
    try:
        existing_payment = order.payment
    except PaymentProof.DoesNotExist:
        existing_payment = None

    if request.method == 'POST':
        form = PaymentProofForm(request.POST, request.FILES, instance=existing_payment)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.order = order
            payment.save()
            return redirect('my_orders')
    else:
        form = PaymentProofForm(instance=existing_payment)

    return render(request, 'core/payment_form.html', {
        'form': form, 
        'order': order,
        'is_update': existing_payment is not None
    })

@login_required
def my_orders(request):
    # Only show orders belonging to the current user
    orders = Order.objects.filter(user=request.user)
    return render(request, 'core/my_orders.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'core/order_detail.html', {'order': order})