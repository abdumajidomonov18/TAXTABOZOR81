from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot.api.cart import cart_api
from bot.keyboards.inline import get_cart_keyboard
from bot.keyboards.reply import get_main_menu_keyboard

router = Router()


def format_cart_message(cart_data: dict) -> tuple[str, list]:
    """Savat ma'lumotlarini chiroyli matn va tugmalar holatiga keltirish."""
    items = cart_data.get("items", [])
    if not items:
        return "🛒 <b>Sizning savatchangiz bo'sh.</b>\n\nMahsulotlarni tanlash uchun '🌲 Katalog' bo'limiga o'ting.", []

    total_price = f"{int(float(cart_data.get('total_price', 0))):,} so'm".replace(",", " ")
    lines = ["🛒 <b>Savatchangizdagi mahsulotlar:</b>\n"]

    for idx, item in enumerate(items, 1):
        prod = item.get("product", {})
        unit = prod.get("unit", {}).get("short_name", "dona")
        price = f"{int(float(prod.get('price', 0))):,} so'm".replace(",", " ")
        subtotal = f"{int(float(item.get('subtotal', 0))):,} so'm".replace(",", " ")
        qty = item.get("quantity", 1)

        lines.append(
            f"{idx}. <b>{prod.get('name')}</b>\n"
            f"   └ {qty} {unit} × {price} = <b>{subtotal}</b>"
        )

    lines.append(f"\n💵 <b>Jami summa:</b> {total_price}")
    return "\n".join(lines), items


@router.message(F.text == "🛒 Savatcha")
@router.callback_query(F.data == "view_cart")
async def show_cart(event: types.Message | types.CallbackQuery, state: FSMContext):
    """Foydalanuvchi savatchasini ko'rsatish."""
    await state.clear()
    telegram_id = event.from_user.id
    cart = await cart_api.get_cart(telegram_id)

    if isinstance(cart, dict) and cart.get("_error"):
        text = "⚠️ Savat ma'lumotlarini yuklashda xatolik yuz berdi."
        if isinstance(event, types.CallbackQuery):
            await event.message.answer(text)
            await event.answer()
        else:
            await event.answer(text)
        return

    text, items = format_cart_message(cart)
    reply_markup = get_cart_keyboard(items)

    if isinstance(event, types.CallbackQuery):
        try:
            await event.message.edit_text(text, reply_markup=reply_markup, parse_mode="HTML")
        except Exception:
            await event.message.answer(text, reply_markup=reply_markup, parse_mode="HTML")
        await event.answer()
    else:
        await event.answer(text, reply_markup=reply_markup, parse_mode="HTML")


@router.callback_query(F.data.startswith("cart_inc:"))
async def cart_increment(callback: types.CallbackQuery):
    """Savatdagi mahsulot sonini 1 taga oshirish."""
    product_id = int(callback.data.split(":")[1])
    telegram_id = callback.from_user.id

    await cart_api.add_to_cart(telegram_id=telegram_id, product_id=product_id, quantity=1)
    cart = await cart_api.get_cart(telegram_id)
    text, items = format_cart_message(cart)
    reply_markup = get_cart_keyboard(items)

    try:
        await callback.message.edit_text(text, reply_markup=reply_markup, parse_mode="HTML")
    except Exception:
        pass
    await callback.answer("Miqdor oshirildi")


@router.callback_query(F.data.startswith("cart_dec:"))
async def cart_decrement(callback: types.CallbackQuery):
    """Savatdagi mahsulot sonini 1 taga kamaytirish."""
    product_id = int(callback.data.split(":")[1])
    telegram_id = callback.from_user.id

    await cart_api.remove_from_cart(telegram_id=telegram_id, product_id=product_id, quantity=1)
    cart = await cart_api.get_cart(telegram_id)
    text, items = format_cart_message(cart)
    reply_markup = get_cart_keyboard(items)

    try:
        await callback.message.edit_text(text, reply_markup=reply_markup, parse_mode="HTML")
    except Exception:
        pass
    await callback.answer("Miqdor kamaytirildi")


@router.callback_query(F.data.startswith("cart_del:"))
async def cart_delete_item(callback: types.CallbackQuery):
    """Mahsulotni savatdan butunlay o'chirish."""
    product_id = int(callback.data.split(":")[1])
    telegram_id = callback.from_user.id

    await cart_api.remove_from_cart(telegram_id=telegram_id, product_id=product_id, quantity=0)
    cart = await cart_api.get_cart(telegram_id)
    text, items = format_cart_message(cart)
    reply_markup = get_cart_keyboard(items)

    try:
        await callback.message.edit_text(text, reply_markup=reply_markup, parse_mode="HTML")
    except Exception:
        pass
    await callback.answer("Mahsulot savatdan o'chirildi", show_alert=True)


@router.callback_query(F.data == "cart_clear")
async def cart_clear(callback: types.CallbackQuery):
    """Savatni to'liq tozalash."""
    telegram_id = callback.from_user.id
    await cart_api.clear_cart(telegram_id)

    text = "🛒 <b>Sizning savatchangiz tozalandi.</b>\n\nMahsulotlarni tanlash uchun '🌲 Katalog' bo'limiga o'ting."
    reply_markup = get_cart_keyboard([])

    try:
        await callback.message.edit_text(text, reply_markup=reply_markup, parse_mode="HTML")
    except Exception:
        pass
    await callback.answer("Savat tozalandi")
