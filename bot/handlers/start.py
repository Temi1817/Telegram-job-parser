from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from bot.database import Database
from bot.keyboards import language_keyboard, main_menu, stats_keyboard
from bot.locales import t, BTN_PAUSE, BTN_RESUME, BTN_HELP, BTN_STATS, BTN_CHANGE_LANG

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, db: Database):
    user = await db.get_user(message.from_user.id)
    if not user:
        await db.create_user(message.from_user.id)
        await message.answer(
            "🌐 Choose language / Выберите язык / Тілді таңдаңыз:",
            reply_markup=language_keyboard(),
        )
    else:
        lang = user['language']
        await message.answer(
            t(lang, 'welcome'),
            reply_markup=main_menu(lang, bool(user['is_active'])),
            parse_mode="Markdown",
        )


@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: CallbackQuery, db: Database):
    lang_map = {"lang_ru": "ru", "lang_kz": "kz", "lang_en": "en"}
    lang = lang_map.get(callback.data, "ru")
    user_id = callback.from_user.id

    user = await db.get_user(user_id)
    if not user:
        await db.create_user(user_id, lang)
    else:
        await db.set_language(user_id, lang)

    await callback.message.edit_text(t(lang, 'language_set'))
    await callback.message.answer(
        t(lang, 'welcome'),
        reply_markup=main_menu(lang, True),
        parse_mode="Markdown",
    )
    await callback.answer()


@router.message(F.text.in_(BTN_PAUSE))
async def btn_pause(message: Message, db: Database):
    user = await db.get_user(message.from_user.id)
    lang = user['language'] if user else 'ru'
    if not user or not user['is_active']:
        await message.answer(t(lang, 'already_paused'), reply_markup=main_menu(lang, False))
        return
    await db.set_active(message.from_user.id, False)
    await message.answer(t(lang, 'paused'), reply_markup=main_menu(lang, False))


@router.message(F.text.in_(BTN_RESUME))
async def btn_resume(message: Message, db: Database):
    user = await db.get_user(message.from_user.id)
    lang = user['language'] if user else 'ru'
    if not user or user['is_active']:
        await message.answer(t(lang, 'already_active'), reply_markup=main_menu(lang, True))
        return
    await db.set_active(message.from_user.id, True)
    await message.answer(t(lang, 'resumed'), reply_markup=main_menu(lang, True))


@router.message(F.text.in_(BTN_HELP))
async def btn_help(message: Message, db: Database):
    user = await db.get_user(message.from_user.id)
    lang = user['language'] if user else 'ru'
    await message.answer(t(lang, 'help'), parse_mode="Markdown")


@router.message(F.text.in_(BTN_STATS))
async def btn_stats(message: Message, db: Database):
    user = await db.get_user(message.from_user.id)
    lang = user['language'] if user else 'ru'
    filters = await db.get_filters(message.from_user.id)
    stats = await db.get_stats(message.from_user.id)

    keywords = (filters or {}).get('keywords') or t(lang, 'not_set')
    is_active = bool(user['is_active']) if user else False
    status = t(lang, 'status_on') if is_active else t(lang, 'status_off')

    text = (
        f"{t(lang, 'stats_title')}\n\n"
        f"{t(lang, 'stats_total', count=stats['total'])}\n"
        f"{t(lang, 'stats_today', count=stats['today'])}\n"
        f"{t(lang, 'stats_week',  count=stats['week'])}\n\n"
        f"{t(lang, 'stats_keywords', keywords=keywords)}\n"
        f"{t(lang, 'stats_active', status=status)}"
    )
    await message.answer(text, reply_markup=stats_keyboard(lang), parse_mode="Markdown")


@router.message(F.text.in_(BTN_CHANGE_LANG))
async def btn_change_lang(message: Message, db: Database):
    user = await db.get_user(message.from_user.id)
    lang = user['language'] if user else 'ru'
    await message.answer(t(lang, 'choose_language'), reply_markup=language_keyboard())
