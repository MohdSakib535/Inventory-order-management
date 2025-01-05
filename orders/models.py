from django.db import models

class Inventory(models.Model):
    product_name = models.CharField(max_length=255, unique=True)
    product_description = models.TextField(blank=True, null=True)
    stock_quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product_name}*{self.stock_quantity}"

    def reduce_stock(self, quantity):
        """
        Reduce stock by the specified quantity.
        """
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            self.save()
        else:
            raise ValueError("Not enough stock available.")

class Order(models.Model):
    customer_name = models.CharField(max_length=255)
    email = models.EmailField()
    product = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} - {self.customer_name}'
