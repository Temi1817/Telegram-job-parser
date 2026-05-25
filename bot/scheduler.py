import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from bot.job_service import JobService

logger = logging.getLogger(__name__)


class JobScheduler:
    def __init__(self, job_service: JobService, interval_minutes: int = 30):
        self.job_service = job_service
        self.interval_minutes = interval_minutes
        self._scheduler = AsyncIOScheduler()

    def start(self):
        self._scheduler.add_job(
            self.job_service.run_for_all_users,
            trigger=IntervalTrigger(minutes=self.interval_minutes),
            id="job_check",
            replace_existing=True,
            misfire_grace_time=120,
        )
        self._scheduler.start()
        logger.info(f"Scheduler started — interval: {self.interval_minutes} min")

    def stop(self):
        self._scheduler.shutdown(wait=False)
        logger.info("Scheduler stopped")
