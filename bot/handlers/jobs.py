from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from bot.database import Database
from bot.job_service import JobService
from bot.locales import t, BTN_SEARCH

router = Router()


async def _run_search(message: Message, db: Database, job_service: JobService):
    user = await db.get_user(message.from_user.id)
    if not user:
        await message.answer("Напиши /start чтобы начать.")
        return
    lang = user['language']

    filters = await db.get_filters(message.from_user.id)
    if not filters or not filters.get('keywords'):
        await message.answer(t(lang, 'setup_filters_first'))
        return

    await message.answer(t(lang, 'searching'))
    count = await job_service.run_for_user(message.from_user.id)
    if count == 0:
        await message.answer(t(lang, 'no_new_jobs'))


@router.message(F.text.in_(BTN_SEARCH))
async def btn_search(message: Message, db: Database, job_service: JobService):
    await _run_search(message, db, job_service)


@router.callback_query(F.data == "search_now")
async def search_now(callback: CallbackQuery, db: Database, job_service: JobService):
    user = await db.get_user(callback.from_user.id)
    lang = user['language'] if user else 'ru'

    filters = await db.get_filters(callback.from_user.id)
    if not filters or not filters.get('keywords'):
        await callback.answer(t(lang, 'setup_filters_first'), show_alert=True)
        return

    await callback.answer()
    await callback.message.answer(t(lang, 'searching'))
    count = await job_service.run_for_user(callback.from_user.id)
    if count == 0:
        await callback.message.answer(t(lang, 'no_new_jobs'))
