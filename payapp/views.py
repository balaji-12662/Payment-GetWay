import razorpay
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@csrf_exempt
def payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')  # Get the amount from the form
        currency = 'INR'

        if amount and amount.strip():
            try:
                # Create an order with Razorpay
                order = client.order.create({'amount': int(amount) * 100, 'currency': currency})
                
                # Pass the order details to the frontend
                context = {
                    'order_id': order['id'],  # Razorpay order ID
                    'amount': amount,  # Original amount
                    'currency': currency,
                    'razorpay_key': settings.RAZORPAY_KEY_ID  # Razorpay API key to use in the JS form
                }
                
                return render(request, 'payment.html', context)
            except Exception as e:
                return render(request, 'payment.html', {'error': str(e)})
        else:
            return render(request, 'payment.html', {'error': 'Amount is required.'})
    
    return render(request, 'payment.html')
