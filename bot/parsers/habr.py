import aiohttp
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

HABR_API = "https://career.habr.com/api/frontend/vacancies"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Referer": "https://career.habr.com/vacancies",
}


def keywords_to_query(keywords: str) -> str:
    """'Python, Django, Backend' → 'Python Django Backend' for Habr full-text search"""
    parts = [k.strip() for k in keywords.split(',') if k.strip()]
    return ' '.join(parts)


class HabrParser:
    SOURCE = "habr"

    async def fetch_vacancies(self, keywords: str, remote: bool = False) -> List[Dict[str, Any]]:
        query = keywords_to_query(keywords)
        params: Dict[str, Any] = {
            "q": query,
            "page": 1,
            "per_page": 20,
            "sort": "date",
        }
        if remote:
            params["remote"] = "true"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    HABR_API,
                    params=params,
                    headers=HEADERS,
                    timeout=aiohttp.ClientTimeout(total=15),
                ) as resp:
                    if resp.status != 200:
                        logger.error(f"Habr Career API returned {resp.status}")
                        return []
                    data = await resp.json()
                    items = data.get("vacancies") or data.get("list") or []
                    return [self._normalize(item) for item in items]
        except Exception as e:
            logger.error(f"Habr fetch error: {e}")
            return []

    def _normalize(self, item: Dict) -> Dict[str, Any]:
        salary = item.get("salary") or {}
        salary_from = salary.get("from") or salary.get("salary_from")
        salary_to = salary.get("to") or salary.get("salary_to")
        salary_str = "не указана"
        if salary_from or salary_to:
            parts = []
            if salary_from:
                parts.append(f"от {int(salary_from):,}")
            if salary_to:
                parts.append(f"до {int(salary_to):,}")
            salary_str = " ".join(parts) + " ₸"

        company = item.get("company") or {}
        locations = item.get("locations") or []
        location_name = (
            locations[0].get("title", "") if locations
            else (item.get("city") or {}).get("title", "Удалённо")
        )

        vacancy_id = str(item.get("id", ""))
        return {
            "id": vacancy_id,
            "source": self.SOURCE,
            "title": item.get("title", ""),
            "company": company.get("title") or company.get("name", ""),
            "location": location_name or "Удалённо",
            "salary": salary_str,
            "salary_from": salary_from,
            "url": f"https://career.habr.com/vacancies/{vacancy_id}",
            "description": (item.get("description") or "")[:600],
            "requirements": item.get("skills_title") or "",
        }
