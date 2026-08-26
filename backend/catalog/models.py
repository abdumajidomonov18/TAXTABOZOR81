from django.db import models


class Category(models.Model):
    """
    Mahsulot kategoriyasi.
    icon — botda inline tugmalarda emoji sifatida, image — WebApp'da banner sifatida.
    order — katalogda ko'rsatish tartibini admin panelidan boshqarish imkonini beradi.
    """
    name = models.CharField(max_length=100, verbose_name="Nomi")
    icon = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="Emoji (bot uchun)"
    )  # Masalan: "🪵", "🧱", "🪨"
    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True,
        verbose_name="Rasm (WebApp banner)"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Tartib raqami"
    )

    class Meta:
        ordering = ['order']
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return f"{self.icon} {self.name}".strip()


class Unit(models.Model):
    """
    Mahsulot o'lchov birligi.
    Admin panelidan kodni o'zgartirmasdan yangi birlik qo'shish mumkin.
    Misol: Metr kub (m³), Dona, Qop (50kg), Metr (m), Tonna (t)
    """
    name = models.CharField(max_length=50, verbose_name="To'liq nomi")
    short_name = models.CharField(max_length=10, verbose_name="Qisqa ko'rinish")

    class Meta:
        verbose_name = "O'lchov birligi"
        verbose_name_plural = "O'lchov birliklari"

    def __str__(self):
        return self.short_name


class Product(models.Model):
    """
    Mahsulot kataloği.
    stock yo'q — mahsulot cheksiz deb hisoblanadi.
    is_active=False — vaqtincha sotishni to'xtatish (o'chirmasdan).
    """
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        verbose_name="Kategoriya"
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.PROTECT,  # Birlik ishlatilayotgan bo'lsa o'chirishga yo'l qo'yilmaydi
        verbose_name="O'lchov birligi"
    )
    name = models.CharField(max_length=255, verbose_name="Nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Narx (so'm)"
    )
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name="Rasm"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Faolmi?"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan sana")

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"

    def __str__(self):
        return f"{self.name} ({self.unit})"


class Banner(models.Model):
    """
    Bosh sahifadagi aksiya va reklama bannerlari.
    """
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="Kichik sarlavha / Izoh")
    tag = models.CharField(max_length=50, default="Aksiya", verbose_name="Teg (masalan: Aksiya, Yangilik)")
    image = models.ImageField(upload_to='banners/', blank=True, null=True, verbose_name="Banner rasmi")
    image_url = models.URLField(max_length=500, blank=True, verbose_name="Rasm havolasi (tashqi URL)")
    button_text = models.CharField(max_length=50, default="Xarid qilish", verbose_name="Tugma matni")
    link = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Havola / Link (masalan: https://t.me/... yoki screen:cart)"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='banners',
        verbose_name="Bog'langan kategoriya"
    )
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")


    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Banner"
        verbose_name_plural = "Bannerlar"

    def __str__(self):
        return self.title

