import logging


logger = logging.getLogger(__name__)


from django.shortcuts import render, get_object_or_404
from .models import Order, Inventory
from .tasks import send_order_confirmation, update_inventory

def place_order(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        product_id = request.POST['product_id']
        quantity = int(request.POST['quantity'])

        product = get_object_or_404(Inventory, id=product_id)

        # Check if stock is sufficient
        if product.stock_quantity < quantity:
            return render(request, 'order_failed.html', {'message': "Not enough stock available."})

        # Save the order
        order = Order.objects.create(
            customer_name=name,
            email=email,
            product=product,
            quantity=quantity,
        )

        # Trigger Celery tasks
        send_order_confirmation.delay(email, order.id)
        update_inventory.delay(product.id, quantity)

        return render(request, 'order_success.html', {'order': order})

    else:
        products = Inventory.objects.all()
        return render(request, 'order_form.html', {'products': products})

