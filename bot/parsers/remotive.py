import aiohttp
import logging
import re
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

REMOTIVE_API = "https://remotive.com/api/remote-jobs"


class RemotiveParser:
    SOURCE = "remotive"

    async def fetch_vacancies(self, keywords: str) -> List[Dict[str, Any]]:
        parts = [k.strip() for k in keywords.split(',') if k.strip()]
        query = parts[0] if parts else (keywords.split()[0] if keywords.split() else '')
        if not query:
            return []

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    REMOTIVE_API,
                    params={"search": query, "limit": 20},
                    headers={"Accept": "application/json"},
                    timeout=aiohttp.ClientTimeout(total=15),
                ) as resp:
                    if resp.status != 200:
                        logger.error(f"Remotive returned {resp.status}")
                        return []
                    data = await resp.json()
                    jobs = data.get("jobs", [])
                    return [self._normalize(j) for j in jobs[:20]]
        except Exception as e:
            logger.error(f"Remotive fetch error: {e}")
            return []

    def _normalize(self, item: Dict) -> Dict[str, Any]:
        salary_str = item.get("salary", "") or "не указана"
        description = re.sub(r"<[^>]+>", "", item.get("description", ""))[:600]
        tags = item.get("tags") or []

        return {
            "id":           str(item.get("id", "")),
            "source":       self.SOURCE,
            "title":        item.get("title", ""),
            "company":      item.get("company_name", ""),
            "location":     item.get("candidate_required_location", "Worldwide") or "Worldwide",
            "salary":       salary_str,
            "salary_from":  None,
            "url":          item.get("url", ""),
            "description":  description,
            "requirements": ", ".join(tags[:10]),
        }
