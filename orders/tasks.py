
from celery.signals import task_prerun, task_postrun
import logging
from orders.models import Inventory
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)



from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from django.conf import settings

@shared_task(name="send order confirmation")
def send_order_confirmation(email, order_id):
    """
    Sends an order confirmation email to the customer.
    """
    subject = "Order Confirmation"
    message = f"Your order #{order_id} has been successfully placed. Thank you for shopping with us!"
    sender = settings.EMAIL_HOST_USER 
    try:
        send_mail(subject, message, sender, [email])
        return f"Order confirmation email sent to {email}."
    except Exception as e:
        return f"Failed to send email to {email}: {str(e)}"


@shared_task(name="update inventory")
def update_inventory(product_id, quantity):
    """
    Updates the inventory stock for a product after an order is placed.
    """
    try:
        product = Inventory.objects.get(id=product_id)
        product.reduce_stock(quantity)
        return f"Inventory updated for {product.product_name}: reduced by {quantity}."
    except Inventory.DoesNotExist:
        return f"Product with ID {product_id} does not exist."
    except ValueError as e:
        return str(e)
    

@shared_task
def send_daily_sales_report():
    """
        Generates and sends a daily sales report to the admin.
        """
    logger.info("Starting daily sales report task")
    today = datetime.now().date()
    orders = Order.objects.filter(order_date__date=today)

    if orders.exists():
        report = "\n".join(
            [f"Order #{order.id} - {order.product.product_name} x {order.quantity}" for order in orders]
        )
    else:
        report = "No sales were made today."

    subject = "Daily Sales Report"
    sender = settings.EMAIL_HOST_USER
    recipient = ["skb939804@gmail.com"]

    send_mail(subject, report, sender, recipient)
    return "Daily sales report sent to admin."