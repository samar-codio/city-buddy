from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from .models import Order, PaymentProof
from .forms import PaymentProofForm


# Create your views here.
def home(request):
    return render(request,'core/home.html')

@login_required
def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES) 
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('submit_payment', order_id=order.id)
    else:
        form = OrderForm(initial={'name': request.user.profile.full_name})
    
    return render(request, 'core/order_form.html', {'form': form})



@login_required
def submit_payment(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    
    if request.method == 'POST':
        form = PaymentProofForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.order = order
            payment.save()
            # Update order status to 'paid' (optional, or wait for admin)
            return redirect('home')
    else:
        form = PaymentProofForm()
        
    return render(request, 'core/payment_form.html', {
        'form': form, 
        'order': order
    })
