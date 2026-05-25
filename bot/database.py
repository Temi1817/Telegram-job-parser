import aiosqlite
from typing import Optional, List, Dict, Any


class Database:
    def __init__(self, db_path: str = "jobs.db"):
        self.db_path = db_path

    async def init(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    language TEXT DEFAULT 'ru',
                    is_active INTEGER DEFAULT 1,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS user_filters (
                    user_id INTEGER PRIMARY KEY,
                    keywords TEXT DEFAULT '',
                    min_salary INTEGER DEFAULT 0,
                    city TEXT DEFAULT '',
                    experience TEXT DEFAULT 'any',
                    vacancy_language TEXT DEFAULT 'any',
                    sources TEXT DEFAULT 'hh,habr,remoteok',
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS sent_vacancies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    vacancy_id TEXT,
                    source TEXT,
                    sent_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, vacancy_id, source)
                )
            """)
            await db.commit()

            # Migration: add sources column to existing databases
            try:
                await db.execute(
                    "ALTER TABLE user_filters ADD COLUMN sources TEXT DEFAULT 'hh,habr,remoteok'"
                )
                await db.commit()
            except Exception:
                pass

    async def get_user(self, user_id: int) -> Optional[Dict]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM users WHERE user_id = ?", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None

    async def create_user(self, user_id: int, language: str = 'ru'):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR IGNORE INTO users (user_id, language) VALUES (?, ?)",
                (user_id, language)
            )
            await db.execute(
                "INSERT OR IGNORE INTO user_filters (user_id) VALUES (?)",
                (user_id,)
            )
            await db.commit()

    async def set_language(self, user_id: int, language: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE users SET language = ? WHERE user_id = ?",
                (language, user_id)
            )
            await db.commit()

    async def set_active(self, user_id: int, is_active: bool):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE users SET is_active = ? WHERE user_id = ?",
                (1 if is_active else 0, user_id)
            )
            await db.commit()

    async def get_filters(self, user_id: int) -> Optional[Dict]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM user_filters WHERE user_id = ?", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None

    async def update_filter(self, user_id: int, field: str, value: Any):
        allowed_fields = {
            'keywords', 'min_salary', 'city', 'experience',
            'vacancy_language', 'sources',
        }
        if field not in allowed_fields:
            raise ValueError(f"Unknown filter field: {field}")
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                f"UPDATE user_filters SET {field} = ? WHERE user_id = ?",
                (value, user_id)
            )
            await db.commit()

    async def is_vacancy_sent(self, user_id: int, vacancy_id: str, source: str) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT 1 FROM sent_vacancies WHERE user_id = ? AND vacancy_id = ? AND source = ?",
                (user_id, vacancy_id, source)
            ) as cursor:
                return await cursor.fetchone() is not None

    async def mark_vacancy_sent(self, user_id: int, vacancy_id: str, source: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR IGNORE INTO sent_vacancies (user_id, vacancy_id, source) VALUES (?, ?, ?)",
                (user_id, vacancy_id, source)
            )
            await db.commit()

    async def get_active_users(self) -> List[Dict]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT u.*, f.keywords, f.min_salary, f.city, f.experience, "
                "f.vacancy_language, f.sources "
                "FROM users u JOIN user_filters f ON u.user_id = f.user_id "
                "WHERE u.is_active = 1 AND f.keywords != ''"
            ) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

    async def get_stats(self, user_id: int) -> Dict[str, int]:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT COUNT(*) FROM sent_vacancies WHERE user_id = ?", (user_id,)
            ) as cur:
                total = (await cur.fetchone())[0]
            async with db.execute(
                "SELECT COUNT(*) FROM sent_vacancies "
                "WHERE user_id = ? AND date(sent_at) = date('now')",
                (user_id,)
            ) as cur:
                today = (await cur.fetchone())[0]
            async with db.execute(
                "SELECT COUNT(*) FROM sent_vacancies "
                "WHERE user_id = ? AND sent_at >= datetime('now', '-7 days')",
                (user_id,)
            ) as cur:
                week = (await cur.fetchone())[0]
        return {"total": total, "today": today, "week": week}

    async def clear_history(self, user_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "DELETE FROM sent_vacancies WHERE user_id = ?", (user_id,)
            )
            await db.commit()
