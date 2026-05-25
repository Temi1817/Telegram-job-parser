from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from bot.database import Database
from bot.keyboards import (
    filters_menu_keyboard, experience_keyboard, vacancy_language_keyboard,
    main_menu, sources_keyboard, EXP_LABELS, VLANG_LABELS,
)
from bot.locales import t, BTN_FILTERS

router = Router()


class FilterStates(StatesGroup):
    waiting_keywords = State()
    waiting_salary   = State()
    waiting_city     = State()


def build_filters_text(lang: str, filters: dict) -> str:
    min_salary = filters.get('min_salary', 0) or 0
    salary_str = f"{int(min_salary):,} KZT" if min_salary else t(lang, 'not_set')

    exp_key   = EXP_LABELS.get(filters.get('experience', 'any'), 'exp_any')
    vlang_key = VLANG_LABELS.get(filters.get('vacancy_language', 'any'), 'lang_any')

    sources_str = filters.get('sources', 'hh,habr,remoteok')
    active_srcs = {s.strip() for s in sources_str.split(',') if s.strip()}
    src_parts = []
    if 'hh' in active_srcs:       src_parts.append('🟡 HH.kz')
    if 'habr' in active_srcs:     src_parts.append('💙 Habr')
    if 'remoteok' in active_srcs: src_parts.append('🌍 Remote')
    if 'djinni' in active_srcs:   src_parts.append('🦎 Djinni')
    if 'remotive' in active_srcs: src_parts.append('🚀 Remotive')
    src_display = ', '.join(src_parts) if src_parts else '—'

    return "\n".join([
        t(lang, 'filters_menu'), "",
        f"🔑 {t(lang, 'filter_keywords')}: *{filters.get('keywords') or t(lang, 'not_set')}*",
        f"💰 {t(lang, 'filter_salary')}: *{salary_str}*",
        f"🏙️ {t(lang, 'filter_city')}: *{filters.get('city') or t(lang, 'not_set')}*",
        f"📊 {t(lang, 'filter_experience')}: *{t(lang, exp_key)}*",
        f"🌐 {t(lang, 'filter_vacancy_lang')}: *{t(lang, vlang_key)}*",
        f"🗂 {t(lang, 'filter_sources')}: {src_display}",
    ])


async def _lang(db: Database, user_id: int) -> str:
    user = await db.get_user(user_id)
    return user['language'] if user else 'ru'


async def _show_filters(message: Message, db: Database, lang: str):
    filters = await db.get_filters(message.from_user.id)
    await message.answer(
        build_filters_text(lang, filters or {}),
        reply_markup=filters_menu_keyboard(lang, filters or {}),
        parse_mode="Markdown",
    )


# ── Open filters menu ──────────────────────────────────────────────────────────

@router.message(F.text.in_(BTN_FILTERS))
async def btn_filters(message: Message, db: Database):
    lang = await _lang(db, message.from_user.id)
    await _show_filters(message, db, lang)


# ── Keywords ───────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "edit_keywords")
async def edit_keywords(callback: CallbackQuery, state: FSMContext, db: Database):
    lang = await _lang(db, callback.from_user.id)
    await callback.message.answer(t(lang, 'set_keywords'), parse_mode="Markdown")
    await state.set_state(FilterStates.waiting_keywords)
    await callback.answer()


@router.message(FilterStates.waiting_keywords)
async def process_keywords(message: Message, state: FSMContext, db: Database):
    lang = await _lang(db, message.from_user.id)
    keywords = message.text.strip()
    await db.update_filter(message.from_user.id, 'keywords', keywords)
    await state.clear()
    await message.answer(t(lang, 'keywords_saved', keywords=keywords), parse_mode="Markdown")
    await _show_filters(message, db, lang)


# ── Salary ─────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "edit_salary")
async def edit_salary(callback: CallbackQuery, state: FSMContext, db: Database):
    lang = await _lang(db, callback.from_user.id)
    await callback.message.answer(t(lang, 'set_salary'), parse_mode="Markdown")
    await state.set_state(FilterStates.waiting_salary)
    await callback.answer()


@router.message(FilterStates.waiting_salary)
async def process_salary(message: Message, state: FSMContext, db: Database):
    lang = await _lang(db, message.from_user.id)
    raw = message.text.strip().replace(" ", "").replace(",", "")
    if not raw.isdigit():
        await message.answer(t(lang, 'invalid_salary'))
        return
    salary = int(raw)
    await db.update_filter(message.from_user.id, 'min_salary', salary)
    await state.clear()
    await message.answer(t(lang, 'salary_saved', salary=f"{salary:,}"), parse_mode="Markdown")
    await _show_filters(message, db, lang)


# ── City ───────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "edit_city")
async def edit_city(callback: CallbackQuery, state: FSMContext, db: Database):
    lang = await _lang(db, callback.from_user.id)
    await callback.message.answer(t(lang, 'set_city'), parse_mode="Markdown")
    await state.set_state(FilterStates.waiting_city)
    await callback.answer()


@router.message(FilterStates.waiting_city)
async def process_city(message: Message, state: FSMContext, db: Database):
    lang = await _lang(db, message.from_user.id)
    city = message.text.strip()
    await db.update_filter(message.from_user.id, 'city', city)
    await state.clear()
    await message.answer(t(lang, 'city_saved', city=city), parse_mode="Markdown")
    await _show_filters(message, db, lang)


# ── Experience ─────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "edit_experience")
async def edit_experience(callback: CallbackQuery, db: Database):
    lang = await _lang(db, callback.from_user.id)
    await callback.message.answer(
        t(lang, 'set_experience'), reply_markup=experience_keyboard(lang)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("exp_"))
async def set_experience(callback: CallbackQuery, db: Database):
    lang = await _lang(db, callback.from_user.id)
    exp_value = callback.data[4:]
    await db.update_filter(callback.from_user.id, 'experience', exp_value)
    label = t(lang, EXP_LABELS.get(exp_value, 'exp_any'))
    await callback.message.answer(
        t(lang, 'experience_saved', experience=label), parse_mode="Markdown"
    )
    filters = await db.get_filters(callback.from_user.id)
    await callback.message.answer(
        build_filters_text(lang, filters or {}),
        reply_markup=filters_menu_keyboard(lang, filters or {}),
        parse_mode="Markdown",
    )
    await callback.answer()


# ── Vacancy language ───────────────────────────────────────────────────────────

@router.callback_query(F.data == "edit_vacancy_lang")
async def edit_vacancy_lang(callback: CallbackQuery, db: Database):
    lang = await _lang(db, callback.from_user.id)
    await callback.message.answer(
        t(lang, 'set_language_filter'), reply_markup=vacancy_language_keyboard(lang)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("vlang_"))
async def set_vacancy_lang(callback: CallbackQuery, db: Database):
    lang = await _lang(db, callback.from_user.id)
    vlang = callback.data[6:]
    await db.update_filter(callback.from_user.id, 'vacancy_language', vlang)
    filters = await db.get_filters(callback.from_user.id)
    await callback.message.answer(
        build_filters_text(lang, filters or {}),
        reply_markup=filters_menu_keyboard(lang, filters or {}),
        parse_mode="Markdown",
    )
    await callback.answer()


# ── Sources ────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "edit_sources")
async def edit_sources(callback: CallbackQuery, db: Database):
    lang = await _lang(db, callback.from_user.id)
    filters = await db.get_filters(callback.from_user.id)
    sources_str = (filters or {}).get('sources', 'hh,habr,remoteok')
    active = {s.strip() for s in sources_str.split(',') if s.strip()}
    await callback.message.edit_text(
        t(lang, 'sources_title'),
        reply_markup=sources_keyboard(lang, active),
        parse_mode="Markdown",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("src_"))
async def toggle_source(callback: CallbackQuery, db: Database):
    lang = await _lang(db, callback.from_user.id)
    source = callback.data[4:]

    filters = await db.get_filters(callback.from_user.id)
    current_str = (filters or {}).get('sources', 'hh,habr,remoteok')
    active = {s.strip() for s in current_str.split(',') if s.strip()}

    if source in active:
        if len(active) <= 1:
            await callback.answer(t(lang, 'no_sources_selected'), show_alert=True)
            return
        active.discard(source)
    else:
        active.add(source)

    await db.update_filter(callback.from_user.id, 'sources', ','.join(sorted(active)))
    await callback.message.edit_reply_markup(reply_markup=sources_keyboard(lang, active))
    await callback.answer()


@router.callback_query(F.data == "back_to_filters")
async def back_to_filters(callback: CallbackQuery, db: Database):
    lang = await _lang(db, callback.from_user.id)
    filters = await db.get_filters(callback.from_user.id)
    await callback.message.edit_text(
        build_filters_text(lang, filters or {}),
        reply_markup=filters_menu_keyboard(lang, filters or {}),
        parse_mode="Markdown",
    )
    await callback.answer()


# ── Reset filters ──────────────────────────────────────────────────────────────

@router.callback_query(F.data == "reset_filters")
async def reset_filters_cb(callback: CallbackQuery, db: Database):
    lang = await _lang(db, callback.from_user.id)
    defaults = [
        ('keywords', ''), ('min_salary', 0), ('city', ''),
        ('experience', 'any'), ('vacancy_language', 'any'),
        ('sources', 'hh,habr,remoteok'),
    ]
    for field, value in defaults:
        await db.update_filter(callback.from_user.id, field, value)

    filters = await db.get_filters(callback.from_user.id)
    await callback.message.edit_text(
        build_filters_text(lang, filters or {}),
        reply_markup=filters_menu_keyboard(lang, filters or {}),
        parse_mode="Markdown",
    )
    await callback.answer(t(lang, 'filters_reset'))


# ── Clear history ──────────────────────────────────────────────────────────────

@router.callback_query(F.data == "clear_history")
async def clear_history_cb(callback: CallbackQuery, db: Database):
    lang = await _lang(db, callback.from_user.id)
    await db.clear_history(callback.from_user.id)
    await callback.answer(t(lang, 'history_cleared'), show_alert=True)
