from django.db import models
from .product import Product
from accounts.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    product_name = models.CharField("Назва товару", max_length=255, editable=False)
    quantity = models.PositiveIntegerField("Кількість", default=1)
    total_price = models.DecimalField("Загальна сума", max_digits=10, decimal_places=2, editable=False)
    customer_name = models.CharField("Ім'я покупця", max_length=255)
    phone = models.CharField("Телефон", max_length=20)

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ['-id']

    def save(self, *args, **kwargs):
        # автоматично заповнюємо назву товару
        if self.product:
            self.product_name = self.product.name
            # автоматично рахуємо суму
            self.total_price = self.product.price * self.quantity

            # зменшуємо кількість товару на складі
            if self.product.stock >= self.quantity:
                self.product.stock -= self.quantity
                self.product.save()
            else:
                raise ValueError("Недостатньо товару на складі")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_name} — {self.product_name} ({self.quantity} шт.)"
