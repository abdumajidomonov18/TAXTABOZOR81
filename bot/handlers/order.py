from datetime import datetime, timezone, timedelta
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot.api.cart import cart_api
from bot.api.users import user_api
from bot.api.orders import order_api
from bot.keyboards.inline import (
    get_addresses_selection_keyboard,
    get_payment_methods_keyboard,
    get_order_confirm_keyboard,
)
from bot.keyboards.reply import (
    get_main_menu_keyboard,
    get_location_keyboard,
    get_skip_or_cancel_keyboard,
    get_name_input_keyboard,
    get_address_title_keyboard,
)

from bot.states.states import OrderStates, AddressStates
from bot.config import settings

router = Router()

PAYMENT_LABELS = {
    "cash": "Naqd pul",
    "payme": "Payme",
    "click": "Click",
}


def build_group_order_notification(order_data: dict) -> str:
    """Ishchilar guruhi va adminlar uchun yangi buyurtma bildirishnomasi."""
    order_id = order_data.get("id")

    # Sana formatlash (O'zbekiston vaqti bilan UTC+5)
    created_at_raw = order_data.get("created_at", "")
    try:
        dt = datetime.fromisoformat(created_at_raw.replace("Z", "+00:00"))
        dt_uz = dt.astimezone(timezone(timedelta(hours=5)))
        formatted_date = dt_uz.strftime("%d.%m.%Y %H:%M")
    except Exception:
        formatted_date = datetime.now().strftime("%d.%m.%Y %H:%M")

    full_name = order_data.get("user_full_name") or "Ko'rsatilmagan"
    phone_number = order_data.get("user_phone_number") or ""
    clean_phone = phone_number.replace("+", "")
    telegram_id = order_data.get("user_telegram_id") or ""

    lat = order_data.get("latitude")
    lon = order_data.get("longitude")
    addr_text = order_data.get("address_text", "Manzil ko'rsatilmagan")

    if lat and lon and float(lat) != 0 and float(lon) != 0:
        address_display = f"{addr_text}\nhttps://www.google.com/maps?q={lat},{lon}"
    else:
        address_display = addr_text

    items = order_data.get("items", [])
    items_text_list = []
    for idx, it in enumerate(items, 1):
        p_name = it.get("product_name", "")
        p_price = f"{int(float(it.get('price', 0))):,} so'm".replace(",", " ")
        p_qty = it.get("quantity", 1)
        p_sub = f"{int(float(it.get('subtotal', 0))):,} so'm".replace(",", " ")
        items_text_list.append(
            f"{idx}. {p_name}\n"
            f"💰 Narx: {p_price}\n"
            f"📊 Miqdor: {p_qty}\n"
            f"💵 Summa: {p_sub}"
        )
    items_block = "\n\n".join(items_text_list)

    total_price = f"{int(float(order_data.get('total_price', 0))):,} so'm".replace(",", " ")
    payment_method = order_data.get("payment_method", "cash")
    payment_label = PAYMENT_LABELS.get(payment_method, "Naqd pul")

    msg = (
        "🆕 <b>YANGI BUYURTMA!</b>\n\n"
        f"📦 <b>Buyurtma:</b> #{order_id}\n"
        f"📅 <b>Sana:</b> {formatted_date}\n\n"
        "👤 <b>MIJOZ MA'LUMOTLARI:</b>\n"
        f"├ <b>Ism:</b> {full_name}\n"
        f"├ <b>Telefon:</b> {clean_phone}\n"
        f"└ <b>User ID:</b> {telegram_id}\n\n"
        "📍 <b>YETKAZISH MANZILI:</b>\n"
        f"{address_display}\n\n"
        "🛒 <b>BUYURTMA TARKIBI:</b>\n\n"
        f"{items_block}\n\n"
        "            ==============================\n"
        f"💳 <b>JAMI SUMMA:</b> {total_price}\n"
        f"💵 <b>TO'LOV TURI:</b> {payment_label}\n"
        "📌 <b>STATUS:</b> ⏳ Kutilmoqda"
    )
    return msg


@router.callback_query(F.data == "checkout_start")
async def start_checkout(callback: types.CallbackQuery, state: FSMContext):
    """Buyurtma berish jarayonini boshlash: Ism-familiya so'rash."""
    telegram_id = callback.from_user.id
    cart = await cart_api.get_cart(telegram_id)

    if not cart or not cart.get("items"):
        await callback.answer("⚠️ Savatchangiz bo'sh. Avval mahsulot qo'shing.", show_alert=True)
        return

    await state.update_data(
        total_price=cart.get("total_price", 0),
        items_count=len(cart.get("items", [])),
    )

    # Foydalanuvchining joriy ismini olish
    user_profile = await user_api.get_user_profile(telegram_id)
    current_name = ""
    if isinstance(user_profile, dict) and not user_profile.get("_error"):
        current_name = user_profile.get("full_name") or ""

    await state.set_state(OrderStates.entering_name)
    await callback.message.delete()
    
    prompt_text = (
        "👤 <b>1-qadam: Ism va familiyangiz</b>\n\n"
        "Buyurtmani rasmiylashtirish uchun to'liq ism va familiyangizni kiriting:\n"
        "(Masalan: <i>Ali Valiyev</i>)"
    )
    if current_name:
        prompt_text += f"\n\n<i>Joriy ism: {current_name}</i>"

    await callback.message.answer(
        prompt_text,
        reply_markup=get_name_input_keyboard(current_name),
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(OrderStates.entering_name, F.text)
async def process_order_name(message: types.Message, state: FSMContext):
    """Kiritilgan ism-familiyani saqlash va manzil bosqichiga o'tish."""
    text = message.text.strip()
    if text == "🔙 Bekor qilish":
        await state.clear()
        await message.answer("Buyurtma jarayoni bekor qilindi.", reply_markup=get_main_menu_keyboard())
        return

    full_name = text.replace("👤 ", "").strip()
    if len(full_name) < 2:
        await message.answer("⚠️ Iltimos, to'liq ism va familiyangizni kiriting:")
        return

    telegram_id = message.from_user.id
    # Backendda foydalanuvchi ismini yangilash
    await user_api.update_user_name(telegram_id, full_name)
    await state.update_data(user_full_name=full_name)

    # 2-bosqich: Manzilni tanlash yoki kiritish
    addresses = await user_api.get_addresses(telegram_id)
    if isinstance(addresses, list) and len(addresses) > 0:
        await state.set_state(OrderStates.selecting_address)
        await message.answer(
            f"Rahmat, <b>{full_name}</b>!\n\n"
            "📍 <b>2-qadam: Yetkazib berish manzilini tanlang</b>\n\n"
            "Mavjud manzillaringizdan birini tanlang yoki yangi manzil matnini yozing:",
            reply_markup=get_addresses_selection_keyboard(addresses),
            parse_mode="HTML"
        )
    else:
        # Hech qanday manzil yo'q bo'lsa — matn yoki GPS orqali so'rash
        await state.set_state(AddressStates.waiting_for_location)
        await message.answer(
            f"Rahmat, <b>{full_name}</b>!\n\n"
            "📍 <b>2-qadam: Yetkazib berish manzili</b>\n\n"
            "Yetkazib berish manzilini matn ko'rinishida yozing (masalan: <i>Chilonzor 9-mavze, 12-uy</i>) yoki pastdagi tugma orqali GPS geolokatsiyangizni yuboring:",
            reply_markup=get_location_keyboard(),
            parse_mode="HTML"
        )


@router.callback_query(F.data == "add_new_addr")
async def ask_new_address_location(callback: types.CallbackQuery, state: FSMContext):
    """Yangi manzil kiritish uchun so'rov."""
    await state.set_state(AddressStates.waiting_for_location)
    await callback.message.answer(
        "📍 <b>Yangi yetkazib berish manzili</b>\n\n"
        "Manzilni yozing (masalan: <i>Yunusobod 4-mavze, 15-uy</i>) yoki pastdagi tugma orqali GPS lokatsiyangizni yuboring:",
        reply_markup=get_location_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(AddressStates.waiting_for_location, F.text)
async def process_address_as_text(message: types.Message, state: FSMContext):
    """Foydalanuvchi manzilni matn sifatida yozib yuborganda: Manzil nomini so'raymiz."""
    text = message.text.strip()
    if text == "🔙 Bekor qilish":
        await state.clear()
        await message.answer("Buyurtma jarayoni bekor qilindi.", reply_markup=get_main_menu_keyboard())
        return

    if len(text) < 3:
        await message.answer("⚠️ Iltimos, aniqroq manzil kiriting (kamida 3 ta belgi):")
        return

    # Tavsiya qilinadigan nom (masalan matnning birinchi so'zi)
    suggested = text.split(",")[0].split()[0].strip()[:20]

    await state.update_data(
        temp_address_text=text,
        temp_latitude=0.0,
        temp_longitude=0.0,
    )
    await state.set_state(AddressStates.waiting_for_title)
    await message.answer(
        f"📍 Manzil qabul qilindi: <b>{text}</b>\n\n"
        "🏷 <b>Ushbu manzilga qisqa nom bering:</b>\n"
        "(Keyingi safar tanlash oson bo'lishi uchun, masalan: <i>Uy</i>, <i>Ishxona</i>, <i>Dalvarzin</i>, <i>Obyekt</i>):",
        reply_markup=get_address_title_keyboard(suggested_title=suggested),
        parse_mode="HTML"
    )


@router.message(AddressStates.waiting_for_location, F.location)
async def process_location_for_address(message: types.Message, state: FSMContext):
    """Yuborilgan geolokatsiyani qabul qilib, unga nom so'raymiz."""
    loc = message.location
    address_text = f"Xarita lokatsiyasi ({loc.latitude:.4f}, {loc.longitude:.4f})"

    await state.update_data(
        temp_address_text=address_text,
        temp_latitude=loc.latitude,
        temp_longitude=loc.longitude,
    )
    await state.set_state(AddressStates.waiting_for_title)
    await message.answer(
        "📍 Geolokatsiya qabul qilindi!\n\n"
        "🏷 <b>Ushbu manzilga qisqa nom bering:</b>\n"
        "(Masalan: <i>Uy</i>, <i>Ishxona</i>, <i>Dalvarzin</i>, <i>Qurilish maydoni</i>):",
        reply_markup=get_address_title_keyboard(),
        parse_mode="HTML"
    )


@router.message(AddressStates.waiting_for_title, F.text)
async def process_address_title(message: types.Message, state: FSMContext):
    """Manzil nomini saqlash va to'lov turiga o'tish."""
    text = message.text.strip()
    if text == "🔙 Bekor qilish":
        await state.clear()
        await message.answer("Buyurtma jarayoni bekor qilindi.", reply_markup=get_main_menu_keyboard())
        return

    title = text
    for prefix in ["🏠 ", "🏢 ", "🏗 ", "📦 ", "📍 "]:
        if title.startswith(prefix):
            title = title[len(prefix):].strip()
            break

    if len(title) < 2:
        title = "Manzil"

    data = await state.get_data()
    temp_address_text = data.get("temp_address_text", title)
    temp_lat = data.get("temp_latitude", 0.0)
    temp_lon = data.get("temp_longitude", 0.0)
    telegram_id = message.from_user.id

    new_addr = await user_api.add_address(
        telegram_id=telegram_id,
        title=title,
        address_text=temp_address_text,
        latitude=temp_lat,
        longitude=temp_lon,
        is_default=True
    )

    if isinstance(new_addr, dict) and not new_addr.get("_error"):
        addr_id = new_addr.get("id")
        full_display = f"{title} — {temp_address_text}" if title != temp_address_text else title
        await state.update_data(
            address_id=addr_id,
            address_text=full_display
        )
        # To'lov turiga o'tish
        await state.set_state(OrderStates.selecting_payment)
        await message.answer(
            f"✅ Manzil saqlandi: <b>{full_display}</b>\n\n💳 <b>3-qadam: To'lov usulini tanlang:</b>",
            reply_markup=get_payment_methods_keyboard(),
            parse_mode="HTML"
        )
    else:
        await message.answer("⚠️ Manzilni saqlashda xatolik yuz berdi. Qaytadan urinib ko'ring.")



@router.callback_query(OrderStates.selecting_address, F.data.startswith("sel_addr:"))
async def process_selected_address(callback: types.CallbackQuery, state: FSMContext):
    """Mavjud manzillardan biri tanlanganda."""
    addr_id = int(callback.data.split(":")[1])
    telegram_id = callback.from_user.id

    addresses = await user_api.get_addresses(telegram_id)
    addr_text = "Tanlangan manzil"
    if isinstance(addresses, list):
        for a in addresses:
            if a.get("id") == addr_id:
                addr_text = a.get('address_text') or a.get('title')
                break

    await state.update_data(address_id=addr_id, address_text=addr_text)
    await state.set_state(OrderStates.selecting_payment)

    await callback.message.edit_text(
        f"📍 Tanlangan manzil: <b>{addr_text}</b>\n\n💳 <b>3-qadam: To'lov usulini tanlang:</b>",
        reply_markup=get_payment_methods_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(OrderStates.selecting_payment, F.data.startswith("pay_method:"))
async def process_payment_method(callback: types.CallbackQuery, state: FSMContext):
    """To'lov usuli tanlanganda."""
    method = callback.data.split(":")[1]
    await state.update_data(payment_method=method)

    await state.set_state(OrderStates.entering_comment)
    await callback.message.delete()
    await callback.message.answer(
        "📝 <b>4-qadam: Izoh kiritish</b>\n\nBuyurtma bo'yicha qo'shimcha istaklaringiz yoki yetkazib berish bo'yicha eslatmangiz bo'lsa yozing (yoki o'tkazib yuboring):",
        reply_markup=get_skip_or_cancel_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(OrderStates.entering_comment)
async def process_order_comment(message: types.Message, state: FSMContext):
    """Izoh kiritilganda yoki o'tkazib yuborilganda xulosani ko'rsatish."""
    if message.text == "🔙 Bekor qilish":
        await state.clear()
        await message.answer("Buyurtma bekor qilindi.", reply_markup=get_main_menu_keyboard())
        return

    comment = "" if message.text == "⏩ O'tkazib yuborish" else message.text.strip()
    await state.update_data(comment=comment)

    data = await state.get_data()
    total_price = f"{int(float(data.get('total_price', 0))):,} so'm".replace(",", " ")
    payment_disp = PAYMENT_LABELS.get(data.get("payment_method", "cash"), "Naqd pul")
    addr_disp = data.get("address_text", "Ko'rsatilmagan")
    full_name_disp = data.get("user_full_name", "Ko'rsatilmagan")
    comment_disp = comment if comment else "Izoh yo'q"

    summary_text = (
        "📋 <b>Buyurtma ma'lumotlarini tasdiqlang:</b>\n\n"
        f"👤 <b>Mijoz:</b> {full_name_disp}\n"
        f"📍 <b>Manzil:</b> {addr_disp}\n"
        f"💳 <b>To'lov turi:</b> {payment_disp}\n"
        f"📝 <b>Izoh:</b> {comment_disp}\n"
        f"💰 <b>Jami to'lov:</b> <b>{total_price}</b>\n\n"
        f"Buyurtmani rasmiylashtirishni tasdiqlaysizmi?"
    )

    await state.set_state(OrderStates.confirming)
    await message.answer(
        summary_text,
        reply_markup=get_order_confirm_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(OrderStates.confirming, F.data == "confirm_order_yes")
async def confirm_order(callback: types.CallbackQuery, state: FSMContext):
    """Buyurtmani tasdiqlash, backendda yaratish va ishchilar guruhiga yuborish."""
    data = await state.get_data()
    telegram_id = callback.from_user.id

    address_id = data.get("address_id")
    payment_method = data.get("payment_method", "cash")
    comment = data.get("comment", "")

    result = await order_api.create_order(
        telegram_id=telegram_id,
        address_id=address_id,
        payment_method=payment_method,
        comment=comment
    )

    if result and not result.get("_error"):
        order_id = result.get("id")
        total_price = f"{int(float(result.get('total_price', 0))):,} so'm".replace(",", " ")
        status_disp = result.get("status_display", "Yangi")

        await state.clear()
        success_text = (
            f"🎉 <b>Buyurtmangiz muvaffaqiyatli qabul qilindi!</b>\n\n"
            f"🆔 <b>Buyurtma raqami:</b> #{order_id}\n"
            f"💰 <b>Jami summa:</b> {total_price}\n"
            f"📊 <b>Holati:</b> {status_disp}\n\n"
            f"Tez orada operatorlarimiz siz bilan bog'lanishadi. Rahmat!"
        )
        await callback.message.edit_text(success_text, parse_mode="HTML")
        await callback.message.answer("Asosiy menyu:", reply_markup=get_main_menu_keyboard())

        # Ishchilar guruhi va adminlar uchun xabar matnini tuzish
        group_notification_text = build_group_order_notification(result)

        # 1. Ishchilar guruhiga yuborish
        if settings.ADMIN_GROUP_CHAT_ID:
            try:
                await callback.bot.send_message(
                    chat_id=settings.ADMIN_GROUP_CHAT_ID,
                    text=group_notification_text,
                    parse_mode="HTML",
                    disable_web_page_preview=False
                )
            except Exception as e:
                print(f"Guruhga xabar yuborishda xatolik ({settings.ADMIN_GROUP_CHAT_ID}): {e}")

        # 2. Alohida adminlarga yuborish
        for admin_id in settings.ADMIN_IDS:
            try:
                await callback.bot.send_message(
                    chat_id=admin_id,
                    text=group_notification_text,
                    parse_mode="HTML",
                    disable_web_page_preview=False
                )
            except Exception as e:
                print(f"Adminga xabar yuborishda xatolik ({admin_id}): {e}")
    else:
        error_msg = result.get("detail", "Xatolik yuz berdi") if isinstance(result, dict) else "Noma'lum xatolik"
        await callback.answer(f"⚠️ Xatolik: {error_msg}", show_alert=True)


@router.callback_query(F.data == "cancel_order")
async def cancel_order_callback(callback: types.CallbackQuery, state: FSMContext):
    """Buyurtmani bekor qilish."""
    await state.clear()
    await callback.message.delete()
    await callback.message.answer("Buyurtma jarayoni bekor qilindi.", reply_markup=get_main_menu_keyboard())
    await callback.answer()
