from django.db import models
from users.models import User
from catalog.models import Product


class Cart(models.Model):
    """
    Foydalanuvchi savati — bitta user, bitta savat (OneToOne).
    Bot ham, WebApp ham shu bitta savatga yozadi/o'qiydi.
    User yaratilganda avtomatik Cart ham yaratiladi (signal orqali).
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name="Foydalanuvchi"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Savat"
        verbose_name_plural = "Savatlar"

    def __str__(self):
        return f"Savat: {self.user}"

    @property
    def total_price(self):
        """Savatdagi barcha mahsulotlar umumiy narxi."""
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_items(self):
        """Savatdagi umumiy mahsulot soni."""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """
    Savatdagi bitta mahsulot.
    unique_together — bitta mahsulot faqat 1 qatorda, miqdor oshganda quantity yangilanadi.
    """
    cart = models.ForeignKey(
        Cart,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name="Savat"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Mahsulot"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Miqdor")

    class Meta:
        unique_together = ('cart', 'product')
        verbose_name = "Savat elementi"
        verbose_name_plural = "Savat elementlari"

    @property
    def subtotal(self):
        """Shu element uchun jami narx."""
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
