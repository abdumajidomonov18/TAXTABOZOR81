from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot.api.catalog import catalog_api
from bot.api.cart import cart_api
from bot.keyboards.inline import (
    get_categories_keyboard,
    get_products_keyboard,
    get_product_detail_keyboard,
)
from bot.keyboards.reply import get_cancel_keyboard, get_main_menu_keyboard
from bot.states.states import SearchStates, ProductStates
from bot.config import settings

router = Router()


@router.message(F.text == "🌲 Katalog")
@router.callback_query(F.data == "back_to_categories")
async def show_categories(event: types.Message | types.CallbackQuery, state: FSMContext):
    """Kategoriyalar ro'yxatini ko'rsatish."""
    await state.clear()
    categories = await catalog_api.get_categories()

    if isinstance(categories, dict) and categories.get("_error"):
        text = "⚠️ Kategoriyalarni yuklashda xatolik yuz berdi."
        if isinstance(event, types.CallbackQuery):
            await event.message.answer(text)
            await event.answer()
        else:
            await event.answer(text)
        return

    text = "🌲 <b>Mahsulotlar katalogi</b>\n\nKerakli bo'limni tanlang:"
    reply_markup = get_categories_keyboard(categories)

    if isinstance(event, types.CallbackQuery):
        await event.message.edit_text(text, reply_markup=reply_markup, parse_mode="HTML")
        await event.answer()
    else:
        await event.answer(text, reply_markup=reply_markup, parse_mode="HTML")


@router.callback_query(F.data.startswith("cat:"))
async def show_category_products(callback: types.CallbackQuery):
    """Tanlangan kategoriya mahsulotlarini ko'rsatish."""
    category_id = int(callback.data.split(":")[1])
    products = await catalog_api.get_products(category_id=category_id)

    if isinstance(products, dict) and products.get("_error"):
        await callback.answer("⚠️ Mahsulotlarni yuklashda xatolik.", show_alert=True)
        return

    if not products:
        await callback.answer("Ushbu bo'limda hozircha mahsulotlar mavjud emas.", show_alert=True)
        return

    cat_name = products[0].get("category_name", "Mahsulotlar")
    text = f"📂 <b>{cat_name}</b> bo'limi mahsulotlari:\n\nBatafsil ko'rish va xarid qilish uchun mahsulotni tanlang:"
    reply_markup = get_products_keyboard(products, category_id)

    await callback.message.edit_text(text, reply_markup=reply_markup, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("prod:"))
async def show_product_detail(callback: types.CallbackQuery):
    """Mahsulot tafsilotlarini chiqarish."""
    product_id = int(callback.data.split(":")[1])
    product = await catalog_api.get_product(product_id)

    if isinstance(product, dict) and product.get("_error"):
        await callback.answer("⚠️ Mahsulot ma'lumotlarini yuklab bo'lmadi.", show_alert=True)
        return

    name = product.get("name", "")
    desc = product.get("description", "") or "Tavsif mavjud emas."
    price = f"{int(float(product.get('price', 0))):,} so'm".replace(",", " ")
    unit = product.get("unit", {}).get("short_name", "dona")
    category_id = product.get("category")
    image_url = product.get("image")

    caption = (
        f"🌲 <b>{name}</b>\n\n"
        f"📝 <b>Tavsif:</b> {desc}\n"
        f"💰 <b>Narxi:</b> {price} / {unit}\n"
    )
    reply_markup = get_product_detail_keyboard(product_id, category_id, quantity=1)

    # Agar rasm bo'lsa
    if image_url:
        full_image_url = image_url if image_url.startswith("http") else f"{settings.BACKEND_HOST}{image_url}"
        try:
            await callback.message.delete()
            await callback.message.answer_photo(
                photo=full_image_url,
                caption=caption,
                reply_markup=reply_markup,
                parse_mode="HTML"
            )
            await callback.answer()
            return
        except Exception:
            pass  # Rasm yuklashda xato bo'lsa, matn sifatida yuboramiz

    await callback.message.edit_text(caption, reply_markup=reply_markup, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("np:"))
async def handle_numpad_click(callback: types.CallbackQuery):
    """Numpad tugmalari bosilganda miqdorni real vaqtda yangilash."""
    _, product_id, category_id, current_qty, action = callback.data.split(":")
    product_id = int(product_id)
    category_id = int(category_id)
    current_qty = int(current_qty)

    if action in "0123456789":
        digit = int(action)
        if current_qty == 0:
            new_qty = digit
        else:
            str_val = f"{current_qty}{digit}"
            if len(str_val) > 7:
                str_val = str_val[:7]
            new_qty = int(str_val)
    elif action == "c":
        new_qty = 0
    elif action == "del":
        str_val = str(current_qty)[:-1]
        new_qty = int(str_val) if str_val else 0
    else:
        new_qty = current_qty

    if new_qty == current_qty and action not in ("c", "del"):
        await callback.answer()
        return

    product = await catalog_api.get_product(product_id)
    if isinstance(product, dict) and product.get("_error"):
        await callback.answer("⚠️ Xatolik", show_alert=True)
        return

    name = product.get("name", "")
    desc = product.get("description", "") or "Tavsif mavjud emas."
    unit_price = float(product.get("price", 0))
    price_str = f"{int(unit_price):,} so'm".replace(",", " ")
    unit = product.get("unit", {}).get("short_name", "dona")
    total_for_qty = f"{int(unit_price * new_qty):,} so'm".replace(",", " ")

    caption = (
        f"🌲 <b>{name}</b>\n\n"
        f"📝 <b>Tavsif:</b> {desc}\n"
        f"💰 <b>Birlik narxi:</b> {price_str} / {unit}\n"
        f"🔢 <b>Tanlangan miqdor:</b> <b>{new_qty:,} {unit}</b> (= <b>{total_for_qty}</b>)\n".replace(",", " ")
    )
    reply_markup = get_product_detail_keyboard(product_id, category_id, quantity=new_qty)

    try:
        if callback.message.caption:
            await callback.message.edit_caption(caption=caption, reply_markup=reply_markup, parse_mode="HTML")
        else:
            await callback.message.edit_text(text=caption, reply_markup=reply_markup, parse_mode="HTML")
    except Exception:
        pass

    await callback.answer(f"{new_qty:,} {unit}".replace(",", " "))


@router.callback_query(F.data.startswith("add_cart:"))
async def add_to_cart(callback: types.CallbackQuery):
    """Savatga mahsulot qo'shish."""
    _, product_id, quantity = callback.data.split(":")
    telegram_id = callback.from_user.id
    product_id = int(product_id)
    quantity = int(quantity)

    if quantity <= 0:
        await callback.answer("⚠️ Iltimos, avval miqdorni 0 dan katta qilib kiriting!", show_alert=True)
        return

    res = await cart_api.add_to_cart(telegram_id=telegram_id, product_id=product_id, quantity=quantity)

    if res and not res.get("_error"):
        formatted_qty = f"{quantity:,}".replace(",", " ")
        await callback.answer(f"🛒 {formatted_qty} ta mahsulot savatga qo'shildi!", show_alert=True)
    else:
        await callback.answer("⚠️ Savatga qo'shishda xatolik yuz berdi.", show_alert=True)




MAIN_BUTTONS = [
    "🌲 Katalog", "🛒 Savatcha", "📦 Buyurtmalarim", "📍 Manzillarim",
    "🔍 Qidiruv", "📞 Bog'lanish", "🔙 Bekor qilish", "⏩ O'tkazib yuborish",
    "📱 Telefon raqamni yuborish", "📍 Joriy manzilni (GPS) yuborish"
]


# --- Qidiruv logikasi ---
@router.message(F.text == "🔍 Qidiruv")
@router.callback_query(F.data == "search_product")
async def start_search(event: types.Message | types.CallbackQuery, state: FSMContext):
    """Qidiruvni boshlash."""
    await state.set_state(SearchStates.waiting_for_query)
    text = "🔍 Qidirmoqchi bo'lgan mahsulot nomini yozing (masalan: <i>taxta</i>, <i>sement</i>, <i>armatura</i>):"

    if isinstance(event, types.CallbackQuery):
        await event.message.answer(text, reply_markup=get_cancel_keyboard(), parse_mode="HTML")
        await event.answer()
    else:
        await event.answer(text, reply_markup=get_cancel_keyboard(), parse_mode="HTML")


@router.message(SearchStates.waiting_for_query, F.text)
@router.message(F.text, ~F.text.startswith("/"))
async def process_search(message: types.Message, state: FSMContext):
    """Qidiruv natijalarini tezkor chiqarish."""
    # Agar foydalanuvchi boshqa FSM holatida bo'lsa (masalan buyurtma/ro'yxatdan o'tish), unga xalal bermaymiz
    current_state = await state.get_state()
    if current_state and not current_state.startswith("SearchStates"):
        return

    query = message.text.strip()
    if query in MAIN_BUTTONS:
        return

    if query == "🔙 Bekor qilish":
        await state.clear()
        await message.answer("Bosh menyu", reply_markup=get_main_menu_keyboard())
        return

    if len(query) < 2:
        return

    products = await catalog_api.get_products(search=query)
    await state.clear()

    if isinstance(products, dict) and products.get("_error") or not products:
        await message.answer(
            f"🔍 '<b>{query}</b>' bo'yicha hech qanday mahsulot topilmadi.\n\n"
            f"Barcha mahsulotlarni ko'rish uchun <b>🌲 Katalog</b> bo'limidan foydalanishingiz mumkin.",
            parse_mode="HTML",
            reply_markup=get_main_menu_keyboard()
        )
        return

    # Natijalarni ko'rsatish
    text = f"🔍 '<b>{query}</b>' bo'yicha topilgan mahsulotlar ({len(products)} ta):"
    cat_id = products[0].get("category", 0) if products else 0
    reply_markup = get_products_keyboard(products, category_id=cat_id)

    await message.answer(text, reply_markup=reply_markup, parse_mode="HTML")

