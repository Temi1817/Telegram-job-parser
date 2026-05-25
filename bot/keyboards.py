from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton,
)
from bot.locales import t

EXP_LABELS = {
    'any': 'exp_any', 'noExperience': 'exp_no',
    'between1And3': 'exp_1_3', 'between3And6': 'exp_3_6', 'moreThan6': 'exp_6',
}
VLANG_LABELS = {'any': 'lang_any', 'ru': 'lang_ru', 'en': 'lang_en'}


def main_menu(lang: str, is_active: bool = True) -> ReplyKeyboardMarkup:
    pause_btn = t(lang, 'btn_pause') if is_active else t(lang, 'btn_resume')
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(lang, 'btn_search')),  KeyboardButton(text=t(lang, 'btn_filters'))],
            [KeyboardButton(text=t(lang, 'btn_stats')),   KeyboardButton(text=pause_btn)],
            [KeyboardButton(text=t(lang, 'btn_change_lang')), KeyboardButton(text=t(lang, 'btn_help'))],
        ],
        resize_keyboard=True,
        persistent=True,
    )


def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский",  callback_data="lang_ru"),
            InlineKeyboardButton(text="🇰🇿 Қазақша", callback_data="lang_kz"),
            InlineKeyboardButton(text="🇬🇧 English",  callback_data="lang_en"),
        ]
    ])


def filters_menu_keyboard(lang: str, filters: dict) -> InlineKeyboardMarkup:
    kw = filters.get('keywords') or ''
    kw_display = (kw[:16] + '…') if len(kw) > 18 else (kw or t(lang, 'not_set'))

    min_sal = filters.get('min_salary') or 0
    sal_display = f"{int(min_sal):,} KZT" if min_sal else t(lang, 'not_set')

    city = filters.get('city') or t(lang, 'not_set')

    exp_key = EXP_LABELS.get(filters.get('experience', 'any'), 'exp_any')
    exp_display = t(lang, exp_key).lstrip('🟢🔵🟣🔴⚪️ ')

    vlang_key = VLANG_LABELS.get(filters.get('vacancy_language', 'any'), 'lang_any')
    vlang_display = t(lang, vlang_key).lstrip('🇷🇺🇬🇧🌍 ')

    sources_str = filters.get('sources', 'hh,habr,remoteok')
    active_srcs = {s.strip() for s in sources_str.split(',') if s.strip()}
    src_parts = []
    if 'hh' in active_srcs:       src_parts.append('HH')
    if 'habr' in active_srcs:     src_parts.append('Habr')
    if 'remoteok' in active_srcs: src_parts.append('Remote')
    if 'djinni' in active_srcs:   src_parts.append('Djinni')
    if 'remotive' in active_srcs: src_parts.append('Remotive')
    src_display = ', '.join(src_parts) if src_parts else '—'

    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"🔑 {t(lang, 'filter_keywords')}: {kw_display}",
            callback_data="edit_keywords",
        )],
        [InlineKeyboardButton(
            text=f"💰 {t(lang, 'filter_salary')}: {sal_display}",
            callback_data="edit_salary",
        )],
        [InlineKeyboardButton(
            text=f"🏙️ {t(lang, 'filter_city')}: {city}",
            callback_data="edit_city",
        )],
        [InlineKeyboardButton(
            text=f"📊 {t(lang, 'filter_experience')}: {exp_display}",
            callback_data="edit_experience",
        )],
        [InlineKeyboardButton(
            text=f"🌐 {t(lang, 'filter_vacancy_lang')}: {vlang_display}",
            callback_data="edit_vacancy_lang",
        )],
        [InlineKeyboardButton(
            text=f"🗂 {t(lang, 'filter_sources')}: {src_display}",
            callback_data="edit_sources",
        )],
        [
            InlineKeyboardButton(text=t(lang, 'btn_reset_filters'),  callback_data="reset_filters"),
            InlineKeyboardButton(text=t(lang, 'btn_clear_history'),  callback_data="clear_history"),
        ],
        [InlineKeyboardButton(text=t(lang, 'btn_search_now'), callback_data="search_now")],
    ])


def experience_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, 'exp_no'),  callback_data="exp_noExperience")],
        [InlineKeyboardButton(text=t(lang, 'exp_1_3'), callback_data="exp_between1And3")],
        [InlineKeyboardButton(text=t(lang, 'exp_3_6'), callback_data="exp_between3And6")],
        [InlineKeyboardButton(text=t(lang, 'exp_6'),   callback_data="exp_moreThan6")],
        [InlineKeyboardButton(text=t(lang, 'exp_any'), callback_data="exp_any")],
    ])


def vacancy_language_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, 'lang_ru'),  callback_data="vlang_ru")],
        [InlineKeyboardButton(text=t(lang, 'lang_en'),  callback_data="vlang_en")],
        [InlineKeyboardButton(text=t(lang, 'lang_any'), callback_data="vlang_any")],
    ])


def sources_keyboard(lang: str, active: set) -> InlineKeyboardMarkup:
    def mark(src: str) -> str:
        return "✅" if src in active else "☐"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{mark('hh')} 🟡 HeadHunter KZ",  callback_data="src_hh")],
        [InlineKeyboardButton(text=f"{mark('habr')} 💙 Habr Career",   callback_data="src_habr")],
        [InlineKeyboardButton(text=f"{mark('remoteok')} 🌍 RemoteOK",  callback_data="src_remoteok")],
        [InlineKeyboardButton(text=f"{mark('djinni')} 🦎 Djinni",      callback_data="src_djinni")],
        [InlineKeyboardButton(text=f"{mark('remotive')} 🚀 Remotive",  callback_data="src_remotive")],
        [InlineKeyboardButton(text=t(lang, 'btn_back_to_filters'),     callback_data="back_to_filters")],
    ])


def stats_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, 'btn_clear_history'), callback_data="clear_history")],
    ])


def vacancy_keyboard(lang: str, url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, 'btn_open_vacancy'), url=url)],
    ])
