from django.db import models


class User(models.Model):
    """
    Telegram foydalanuvchisi. Har qanday amal uchun avval shu model yaratiladi.
    Django'ning standart User modeli ishlatilmaydi — chunki bizga password shart emas,
    autentifikatsiya Telegram orqali amalga oshadi.
    """
    telegram_id = models.BigIntegerField(unique=True, verbose_name="Telegram ID")
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Telefon raqam"
    )
    full_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="To'liq ism"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ro'yxatdan o'tgan sana")

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    def __str__(self):
        return f"{self.full_name or 'Nomsiz'} ({self.telegram_id})"


class Address(models.Model):
    """
    Foydalanuvchining yetkazib berish manzillari.
    Bir userda bir nechta manzil bo'lishi mumkin: Uy, Ish, Do'kon va h.k.
    latitude/longitude WebApp'da Telegram geolokatsiyasi orqali olinadi.
    """
    user = models.ForeignKey(
        User,
        related_name='addresses',
        on_delete=models.CASCADE,
        verbose_name="Foydalanuvchi"
    )
    title = models.CharField(
        max_length=100,
        default="Uy",
        verbose_name="Manzil nomi"
    )  # "Uy", "Ish", "Do'kon"
    address_text = models.CharField(
        max_length=500,
        verbose_name="Manzil matni"
    )  # Ko'cha, uy raqami, orientir
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        default=0,
        blank=True,
        null=True,
        verbose_name="Kenglik (lat)"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        default=0,
        blank=True,
        null=True,
        verbose_name="Uzunlik (lon)"
    )

    is_default = models.BooleanField(
        default=False,
        verbose_name="Asosiy manzil"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Manzil"
        verbose_name_plural = "Manzillar"

    def save(self, *args, **kwargs):
        # Agar bu manzil asosiy bo'lsa, xuddi shu userdagi boshqa asosiy manzillarni o'chirish
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} — {self.user}"
