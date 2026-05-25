import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import Config
from bot.database import Database
from bot.handlers import filters, jobs, start
from bot.job_service import JobService
from bot.scheduler import JobScheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    config = Config()

    if not config.BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set. Copy .env.example to .env and fill it in.")

    db = Database(config.DATABASE_PATH)
    await db.init()

    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    job_service = JobService(bot, db)
    scheduler = JobScheduler(job_service, config.UPDATE_INTERVAL_MINUTES)

    dp.include_router(start.router)
    dp.include_router(filters.router)
    dp.include_router(jobs.router)

    scheduler.start()
    logger.info("Bot is running...")

    try:
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            db=db,
            job_service=job_service,
        )
    finally:
        scheduler.stop()
        await bot.session.close()
        logger.info("Bot stopped.")


if __name__ == "__main__":
    asyncio.run(main())
