# TAXTABOZOR81 / G'isht Bozor — Telegram WebApp Frontend

Ushbu frontend dizaynlari **G'isht Bozor / TAXTABOZOR81** loyihasi uchun taqdim etilgan skrinshotlar va dizayn qo'llanmasi (`DESIGN.md`) asosida to'liq yuqori sifatda (pixel-perfect) ishlab chiqildi.

## 📱 Asosiy xususiyatlar

1. **Birlashtirilgan Interaktiv WebApp (`frontend/index.html`)**:
   - Barcha 9 ta ekran (Bosh sahifa, Mahsulot ma'lumoti, Savat, Buyurtma berish, Buyurtmalarim, Buyurtma tafsilotlari, Profil, Sevimlilar, Manzil qo'shish) bitta tezkor SPA (Single Page Application) tizimida ishlaydi.
   - Haqiqiy holat boshqaruvi (State management): Mahsulotlarni qidirish, kategoriyalar bo'yicha saralash, savatga qo'shish/kamaytirish/o'chirish, sevimlilarga saqlash, manzil qo'shish, buyurtma berish va yetkazish statusini kuzatish.
   - **Telegram WebApp SDK** qo'llab-quvvatlashi (`ready()`, `expand()`, haptic tebranishlar, xavfsiz maydonlar).
   - Yuqori sifatli rasmlar va **Material Symbols** piktogrammalari.

2. **Alohida Ekranlar Katalogi (`frontend/stitch_stroymart_telegram_webapp/`)**:
   - `bosh_sahifa_home/` — Asosiy katalog, aksiya bannerlari, tavsiya etilgan va barcha mahsulotlar tarmog'i.
   - `mahsulot_tafsilotlari_product_detail/` — Mahsulot kartasi, texnik xususiyatlar, miqdor kalkulyatori va savatga qo'shish.
   - `savat_cart/` — Savatchadagi mahsulotlar ro'yxati, hisob-kitob va buyurtma berish tugmasi.
   - `buyurtma_berish_checkout/` — Manzil tanlash, to'lov usuli (Naqd, Payme, Click), izoh va yakuniy tasdiqlash.
   - `buyurtmalar_orders/` — Buyurtmalar ro'yxati va holat filtrlari (Barchasi, Faol, Yakunlangan).
   - `buyurtma_tafsilotlari_order_detail/` — Yetkazib berish bosqichlari (Timeline tracker: Yangi ➔ Tasdiqlangan ➔ Yetkazilmoqda ➔ Yakunlangan).
   - `profil_profile/` — Foydalanuvchi ma'lumotlari, menyu bo'limlari va chiqish tugmasi.
   - `sevimlilar_favorites/` — Saqlangan mahsulotlar ro'yxati va tezkor savatga qo'shish.
   - `manzil_qo_shish_add_address/` — Xarita orqali manzilni aniqlash va saqlash.

## 🚀 Qanday ishga tushiriladi?

1. Brauzerda to'g'ridan-to'g'ri ko'rish:
   - `frontend/index.html` faylini istalgan brauzerda oching.
2. Yoki oddiy lokal server orqali:
   ```bash
   npx serve frontend
   # yoki
   python -m http.server 3000 --directory frontend
   ```
