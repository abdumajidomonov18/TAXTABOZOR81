from django.db import models
from users.models import User, Address
from catalog.models import Product, Unit


class Order(models.Model):
    """
    Buyurtma. Cart'dan yaratiladi, savat tozalanadi.
    Manzil ma'lumotlari "snapshot" qilinadi — user keyinchalik manzilni o'zgartirsayam,
    eski buyurtma manzili o'zgarmaydi.
    """
    STATUS_CHOICES = [
        ('new', '🆕 Yangi'),
        ('confirmed', '✅ Tasdiqlangan'),
        ('delivering', '🚚 Yetkazilmoqda'),
        ('done', '✔️ Yakunlangan'),
        ('cancelled', '❌ Bekor qilingan'),
    ]

    PAYMENT_CHOICES = [
        ('cash', 'Naqd pul'),
        ('payme', 'Payme'),
        ('click', 'Click'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Foydalanuvchi"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Holat"
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='cash',
        verbose_name="To'lov usuli"
    )

    # Manzil FK (foydalanuvchi manzilni o'chirsayam, ORDER.SET_NULL qiladi)
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Manzil (FK)"
    )
    # Manzil snapshot — buyurtma paytidagi holat muzlatiladi
    address_text = models.CharField(max_length=500, verbose_name="Manzil matni (snapshot)")
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        verbose_name="Kenglik (snapshot)"
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        verbose_name="Uzunlik (snapshot)"
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Jami narx (so'm)"
    )
    comment = models.TextField(blank=True, verbose_name="Izoh")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Buyurtma sanasi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Oxirgi yangilanish")

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ['-created_at']

    def __str__(self):
        return f"#{self.pk} — {self.user} ({self.get_status_display()})"


class OrderItem(models.Model):
    """
    Buyurtma elementi. Mahsulot narxi va birligi snapshot qilinadi —
    agar keyinchalik narx o'zgarsa, eski buyurtma narxi o'zgarmaydi.
    """
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name="Buyurtma"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,  # Mahsulot hech qachon buyurtma bo'lsa o'chirilmaydi
        verbose_name="Mahsulot"
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.PROTECT,
        verbose_name="O'lchov birligi (snapshot)"
    )
    product_name = models.CharField(max_length=255, verbose_name="Mahsulot nomi (snapshot)")
    quantity = models.PositiveIntegerField(verbose_name="Miqdor")
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Birlik narxi (snapshot, so'm)"
    )

    class Meta:
        verbose_name = "Buyurtma elementi"
        verbose_name_plural = "Buyurtma elementlari"

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product_name} x {self.quantity} ({self.unit})"
