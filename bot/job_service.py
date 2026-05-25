import asyncio
import html
import logging
from typing import Dict, List

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database import Database
from bot.locales import t
from bot.parsers.hh import HHParser
from bot.parsers.habr import HabrParser
from bot.parsers.remoteok import RemoteOKParser
from bot.parsers.djinni import DjinniParser
from bot.parsers.remotive import RemotiveParser

logger = logging.getLogger(__name__)

MAX_PER_RUN = 5

SOURCE_LABELS = {
    'hh':       '🟡 HH.kz',
    'habr':     '💙 Habr Career',
    'remoteok': '🌍 RemoteOK',
    'djinni':   '🦎 Djinni',
    'remotive': '🚀 Remotive',
}


async def _empty() -> List:
    return []


class JobService:
    def __init__(self, bot: Bot, db: Database):
        self.bot = bot
        self.db = db
        self.hh = HHParser()
        self.habr = HabrParser()
        self.remoteok = RemoteOKParser()
        self.djinni = DjinniParser()
        self.remotive = RemotiveParser()

    async def _fetch_all(self, filters: Dict) -> List[Dict]:
        keywords   = filters.get('keywords', '')
        experience = filters.get('experience', 'any')
        city       = filters.get('city', '')
        min_salary = filters.get('min_salary', 0) or 0
        is_remote  = city.lower() in ('удалённо', 'remote', 'қашықтан')

        sources_str   = filters.get('sources') or 'hh,habr,remoteok'
        active_sources = {s.strip() for s in sources_str.split(',') if s.strip()}

        hh_coro = (
            self.hh.fetch_vacancies(keywords, experience=experience, city=city, min_salary=min_salary)
            if 'hh' in active_sources else _empty()
        )
        habr_coro = (
            self.habr.fetch_vacancies(keywords, remote=is_remote)
            if 'habr' in active_sources else _empty()
        )
        remote_coro = (
            self.remoteok.fetch_vacancies(keywords)
            if 'remoteok' in active_sources else _empty()
        )
        djinni_coro = (
            self.djinni.fetch_vacancies(keywords, experience=experience)
            if 'djinni' in active_sources else _empty()
        )
        remotive_coro = (
            self.remotive.fetch_vacancies(keywords)
            if 'remotive' in active_sources else _empty()
        )

        hh_result, habr_result, remote_result, djinni_result, remotive_result = await asyncio.gather(
            hh_coro, habr_coro, remote_coro, djinni_coro, remotive_coro,
            return_exceptions=True,
        )

        pools: List[List[Dict]] = []
        for result in (hh_result, habr_result, remote_result, djinni_result, remotive_result):
            if isinstance(result, list):
                pools.append(result)
            else:
                logger.error(f"Parser exception: {result}")
                pools.append([])

        # Interleave round-robin so all sources get a fair share
        vacancies: List[Dict] = []
        max_len = max((len(p) for p in pools), default=0)
        for i in range(max_len):
            for pool in pools:
                if i < len(pool):
                    vacancies.append(pool[i])

        total = sum(len(p) for p in pools)
        logger.info(f"Fetched {total} vacancies for '{keywords}' (sources: {active_sources})")
        return vacancies

    def _is_relevant(self, vacancy: Dict, filters: Dict) -> bool:
        min_salary = filters.get('min_salary', 0) or 0
        if min_salary:
            salary_from = vacancy.get('salary_from')
            if salary_from is not None and salary_from < min_salary:
                return False

        keywords = [k.strip().lower() for k in filters.get('keywords', '').split(',') if k.strip()]
        if not keywords:
            return True

        text = ' '.join([
            vacancy.get('title', ''),
            vacancy.get('description', ''),
            vacancy.get('requirements', ''),
            vacancy.get('company', ''),
        ]).lower()

        for kw in keywords:
            words = kw.split()
            if all(w in text for w in words):
                return True
        return False

    def _format_vacancy(self, vacancy: Dict, lang: str) -> str:
        def e(val: str) -> str:
            return html.escape(str(val)) if val else ''

        source_label = SOURCE_LABELS.get(vacancy.get('source', ''), '')
        salary = vacancy.get('salary') or t(lang, 'salary_not_set')

        return (
            f"💼 <b>{e(vacancy.get('title', ''))}</b>\n"
            f"🏢 {e(vacancy.get('company', ''))}\n"
            f"📍 {e(vacancy.get('location', ''))}\n"
            f"💰 {e(salary)}\n"
            f"🏷 {source_label}"
        )

    async def process_user(self, user: Dict) -> int:
        user_id: int = user['user_id']
        lang: str = user.get('language', 'ru')
        filters = {
            'keywords':         user.get('keywords', ''),
            'min_salary':       user.get('min_salary', 0),
            'city':             user.get('city', ''),
            'experience':       user.get('experience', 'any'),
            'vacancy_language': user.get('vacancy_language', 'any'),
            'sources':          user.get('sources', 'hh,habr,remoteok'),
        }

        if not filters['keywords']:
            return 0

        vacancies = await self._fetch_all(filters)
        sent_count = 0

        for vacancy in vacancies:
            if sent_count >= MAX_PER_RUN:
                break

            vacancy_id = vacancy.get('id', '')
            source = vacancy.get('source', '')
            if not vacancy_id:
                continue
            if await self.db.is_vacancy_sent(user_id, vacancy_id, source):
                continue

            if not self._is_relevant(vacancy, filters):
                await self.db.mark_vacancy_sent(user_id, vacancy_id, source)
                continue

            await self.db.mark_vacancy_sent(user_id, vacancy_id, source)

            try:
                text = self._format_vacancy(vacancy, lang)
                url = vacancy.get('url', '')
                markup = InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(text=t(lang, 'btn_open_vacancy'), url=url)
                ]]) if url else None

                await self.bot.send_message(
                    user_id, text,
                    parse_mode="HTML",
                    reply_markup=markup,
                )
                sent_count += 1
                await asyncio.sleep(0.3)
            except TelegramForbiddenError:
                await self.db.set_active(user_id, False)
                break
            except Exception as e:
                logger.error(f"Send error for user {user_id}: {e}")

        return sent_count

    async def run_for_all_users(self):
        users = await self.db.get_active_users()
        logger.info(f"Scheduler run: {len(users)} active user(s)")
        for user in users:
            try:
                count = await self.process_user(user)
                logger.info(f"Sent {count} vacancies to user {user['user_id']}")
            except Exception as e:
                logger.error(f"Error for user {user.get('user_id')}: {e}")
            await asyncio.sleep(1)

    async def run_for_user(self, user_id: int) -> int:
        user_data = await self.db.get_user(user_id)
        filters_data = await self.db.get_filters(user_id)
        if not user_data or not filters_data:
            return 0
        return await self.process_user({**user_data, **filters_data})
