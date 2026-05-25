import aiohttp
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

REMOTEOK_API = "https://remoteok.com/api"


class RemoteOKParser:
    SOURCE = "remoteok"

    async def fetch_vacancies(self, keywords: str) -> List[Dict[str, Any]]:
        # Build tag list from comma-separated keywords (up to 3 tags)
        parts = [k.strip().lower() for k in keywords.split(',') if k.strip()]
        tags = "+".join(parts[:3]) if parts else keywords.lower().split()[0]
        params = {"tags": tags}
        headers = {"User-Agent": "Mozilla/5.0 (compatible; ITJobsBot/1.0)"}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    REMOTEOK_API,
                    params=params,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=15),
                ) as resp:
                    if resp.status != 200:
                        logger.error(f"RemoteOK returned {resp.status}")
                        return []
                    data = await resp.json(content_type=None)
                    # First item is metadata, skip it
                    jobs = [j for j in data if isinstance(j, dict) and j.get("position")]
                    return [self._normalize(j) for j in jobs[:20]]
        except Exception as e:
            logger.error(f"RemoteOK fetch error: {e}")
            return []

    def _normalize(self, item: Dict) -> Dict[str, Any]:
        salary_str = "не указана"
        if item.get("salary_min") or item.get("salary_max"):
            parts = []
            if item.get("salary_min"):
                parts.append(f"от ${item['salary_min']:,}")
            if item.get("salary_max"):
                parts.append(f"до ${item['salary_max']:,}")
            salary_str = " ".join(parts)

        return {
            "id": str(item.get("id", item.get("slug", ""))),
            "source": self.SOURCE,
            "title": item.get("position", ""),
            "company": item.get("company", ""),
            "location": "Remote",
            "salary": salary_str,
            "url": item.get("url", f"https://remoteok.com/l/{item.get('slug','')}"),
            "description": item.get("description", "")[:600],
            "requirements": ", ".join(item.get("tags", [])[:10]),
        }
