import aiohttp
import logging
from bs4 import BeautifulSoup
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

DJINNI_URL = "https://djinni.co/jobs/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml",
}

EXP_MAP = {
    'noExperience': 'no_exp',
    'between1And3': '1y',
    'between3And6': '3y',
    'moreThan6':    '5y',
}


class DjinniParser:
    SOURCE = "djinni"

    async def fetch_vacancies(
        self, keywords: str, experience: str = 'any'
    ) -> List[Dict[str, Any]]:
        parts = [k.strip() for k in keywords.split(',') if k.strip()]
        if not parts:
            return []

        params: Dict[str, Any] = {"primary_keyword": parts[0]}
        if len(parts) > 1:
            params["keywords"] = " ".join(parts[1:])
        if experience in EXP_MAP:
            params["exp_level"] = EXP_MAP[experience]

        try:
            async with aiohttp.ClientSession(headers=HEADERS) as session:
                async with session.get(
                    DJINNI_URL,
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=15),
                ) as resp:
                    if resp.status != 200:
                        logger.error(f"Djinni returned {resp.status}")
                        return []
                    html = await resp.text()
                    return self._parse(html)
        except Exception as e:
            logger.error(f"Djinni fetch error: {e}")
            return []

    def _parse(self, html: str) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(html, "html.parser")
        results = []

        for item in soup.select("li.job-list-item")[:20]:
            link_tag = item.select_one("a.job-list-item__link")
            if not link_tag:
                continue

            title = link_tag.get_text(strip=True)
            href = link_tag.get("href", "")
            # ID is the numeric part at the start of the slug
            slug = href.strip("/").split("/")[-1]
            vacancy_id = slug.split("-")[0] if slug else ""
            url = f"https://djinni.co{href}" if href.startswith("/") else href

            company_tag = item.select_one("a.job-list-item__company-link")
            company = company_tag.get_text(strip=True) if company_tag else ""

            salary_tag = item.select_one("span.job-list-item__salary")
            salary = salary_tag.get_text(strip=True) if salary_tag else "не указана"

            loc_tag = item.select_one(".location-text, span.job-list-item__location")
            location = loc_tag.get_text(strip=True) if loc_tag else "Remote"

            if not title or not url:
                continue

            results.append({
                "id":           vacancy_id or url,
                "source":       self.SOURCE,
                "title":        title,
                "company":      company,
                "location":     location,
                "salary":       salary or "не указана",
                "salary_from":  None,
                "url":          url,
                "description":  "",
                "requirements": "",
            })

        return results
