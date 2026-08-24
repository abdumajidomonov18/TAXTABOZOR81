from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.api.users import user_api
from bot.keyboards.reply import get_main_menu_keyboard, get_contact_keyboard
from bot.states.states import RegistrationStates

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    """Botni ishga tushirish va foydalanuvchini tekshirish."""
    await state.clear()
    telegram_id = message.from_user.id
    full_name = message.from_user.full_name or ""

    user_data = await user_api.get_user_profile(telegram_id)

    # Agar foydalanuvchi backendda mavjud bo'lsa
    if user_data and not user_data.get("_error"):
        await message.answer(
            f"Assalomu alaykum, <b>{full_name}</b>!\n"
            f"<b>TAXTABOZOR81</b> rasmiy botiga xush kelibsiz.\n\n"
            f"Qurilish mollari va taxta mahsulotlarini qulay narxlarda xarid qiling.",
            parse_mode="HTML",
            reply_markup=get_main_menu_keyboard()
        )
    else:
        # Ro'yxatdan o'tmagan bo'lsa — telefon raqamini so'rash
        await state.set_state(RegistrationStates.waiting_for_contact)
        await message.answer(
            f"Assalomu alaykum, <b>{full_name}</b>!\n"
            f"<b>TAXTABOZOR81</b> botidan foydalanish uchun telefon raqamingizni yuboring:",
            parse_mode="HTML",
            reply_markup=get_contact_keyboard()
        )


@router.message(RegistrationStates.waiting_for_contact, F.contact)
async def process_contact(message: types.Message, state: FSMContext):
    """Telefon raqam qabul qilinganda ro'yxatdan o'tkazish."""
    contact = message.contact
    telegram_id = message.from_user.id
    phone_number = contact.phone_number
    if not phone_number.startswith("+"):
        phone_number = f"+{phone_number}"

    full_name = f"{contact.first_name or ''} {contact.last_name or ''}".strip() or message.from_user.full_name

    res = await user_api.register_user(
        telegram_id=telegram_id,
        phone_number=phone_number,
        full_name=full_name
    )

    if res and not res.get("_error"):
        await state.clear()
        await message.answer(
            f"✅ Rahmat! Siz muvaffaqiyatli ro'yxatdan o'tdingiz.\n\n"
            f"Endi katalogdan kerakli mahsulotlarni tanlashingiz mumkin.",
            reply_markup=get_main_menu_keyboard()
        )
    else:
        await message.answer(
            "⚠️ Ro'yxatdan o'tishda xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring yoki /start ni bosing."
        )
