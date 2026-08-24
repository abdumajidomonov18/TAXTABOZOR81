# TAXTABOZOR81 — Telegram Bot

Ushbu Telegram bot TAXTABOZOR81 Django REST API backendiga ulanib, foydalanuvchilarga to'g'ridan-to'g'ri Telegram orqali katalog ko'rish, savatchaga mahsulot yig'ish, manzil kiritish va buyurtma rasmiylashtirish imkonini beradi.

## 🛠 Texnologiyalar
- **Python 3.11+**
- **aiogram 3.x**
- **httpx** (asinxron HTTP mijoz)
- **pydantic-settings**

---

## 🚀 O'rnatish va Ishga tushirish

### 1. Kutubxonalarni o'rnatish
Backend uchun ishlatilayotgan venv muhitida yoki alohida muhitda bot kutubxonalarini o'rnating:

```bash
pip install -r bot/requirements.txt
```

### 2. `.env` faylini sozlash
`bot/.env` faylini oching va bot tokenini kiriting:

```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ
API_BASE_URL=http://127.0.0.1:8000/api
BACKEND_HOST=http://127.0.0.1:8000
ADMIN_IDS=[123456789]
```

### 3. Backendni ishga tushirish
Avval Django backend serverini ishga tushiring:
```bash
cd backend
python manage.py runserver
```

### 4. Botni ishga tushirish
Loyiha ildizidan turib botni ishga tushiring:
```bash
python -m bot.main
```

---

## 📂 Tuzilishi
- `bot/api/` — Django REST API bilan muloqot qiluvchi asinxron modullar.
- `bot/handlers/` — Bot komandalari, katalog, savat, buyurtma va tarix handlerlari.
- `bot/keyboards/` — Reply va Inline klaviaturalar.
- `bot/states/` — FSM (Finite State Machine) holatlari.
- `bot/config.py` — Sozlamalar.
- `bot/main.py` — Ishga tushirish nuqtasi.
