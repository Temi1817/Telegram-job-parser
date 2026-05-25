import re
import logging
from typing import List, Dict, Any

import aiohttp

logger = logging.getLogger(__name__)

HH_SEARCH = "https://hh.kz/search/vacancy"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ru-RU,ru;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

EXPERIENCE_MAP = {
    "noExperience":   "noExperience",
    "between1And3":   "between1And3",
    "between3And6":   "between3And6",
    "moreThan6":      "moreThan6",
}


def _strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).strip()


def keywords_to_query(keywords: str) -> str:
    parts = [k.strip() for k in keywords.split(",") if k.strip()]
    return " OR ".join(parts) if len(parts) > 1 else (parts[0] if parts else "")


class HHParser:
    SOURCE = "hh"

    async def fetch_vacancies(
        self, keywords: str, experience: str = "any", city: str = "",
        min_salary: int = 0
    ) -> List[Dict[str, Any]]:
        query = keywords_to_query(keywords)
        if not query:
            return []

        params: Dict[str, Any] = {
            "text": query,
            "area": "40",
            "per_page": "20",
            "order_by": "publication_time",
        }
        if experience in EXPERIENCE_MAP:
            params["experience"] = EXPERIENCE_MAP[experience]
        if city and city.lower() in ("удалённо", "remote", "қашықтан"):
            params["schedule"] = "remote"
        if min_salary:
            params["salary"] = str(min_salary)
            params["only_with_salary"] = "true"

        try:
            async with aiohttp.ClientSession(headers=HEADERS) as session:
                async with session.get(
                    HH_SEARCH,
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=15),
                ) as resp:
                    if resp.status != 200:
                        logger.error(f"HH website returned {resp.status}")
                        return []
                    html = await resp.text(encoding="utf-8")
                    return self._parse_html(html)
        except Exception as e:
            logger.error(f"HH fetch error: {e}")
            return []

    def _parse_html(self, html: str) -> List[Dict[str, Any]]:
        titles = re.findall(
            r'data-qa="serp-item__title-text"[^>]*>([^<]+)', html
        )
        # URLs contain vacancy IDs: almaty.hh.kz/vacancy/123 or hh.kz/vacancy/123
        url_matches = re.findall(
            r'href="(https://[^"]*hh\.kz/vacancy/(\d+))[^"]*"', html
        )
        # Deduplicate while preserving order
        seen: set = set()
        vacancy_pairs: List[tuple] = []
        for url, vid in url_matches:
            if vid not in seen:
                seen.add(vid)
                vacancy_pairs.append((vid, f"https://hh.kz/vacancy/{vid}"))

        salaries = re.findall(
            r'data-qa="vacancy-serp__compensation"[^>]*>(.*?)</span>',
            html, re.DOTALL
        )
        companies = re.findall(
            r'data-qa="vacancy-serp__vacancy-employer-text"[^>]*>(.*?)</span>',
            html, re.DOTALL
        )
        addresses = re.findall(
            r'data-qa="vacancy-serp__vacancy-address"[^>]*>([^<]+)', html
        )

        results = []
        for i, (vid, url) in enumerate(vacancy_pairs):
            title = titles[i].strip() if i < len(titles) else ""
            salary_raw = _strip_tags(salaries[i]) if i < len(salaries) else ""
            company = _strip_tags(companies[i]) if i < len(companies) else ""
            location = addresses[i].strip() if i < len(addresses) else "Казахстан"

            salary_str, salary_from = self._parse_salary(salary_raw)

            results.append({
                "id": vid,
                "source": self.SOURCE,
                "title": title,
                "company": company,
                "location": location,
                "salary": salary_str,
                "salary_from": salary_from,
                "url": url,
                "description": "",
                "requirements": "",
            })
        return results

    def _parse_salary(self, raw: str) -> tuple:
        """Returns (salary_str, salary_from_int_or_None)."""
        if not raw:
            return "не указана", None

        raw = raw.replace(" ", " ").replace("  ", " ").strip()
        salary_from = None

        m_from = re.search(r"от\s+([\d\s]+)", raw, re.IGNORECASE)
        if m_from:
            try:
                salary_from = int(m_from.group(1).replace(" ", ""))
            except ValueError:
                pass

        return raw, salary_from
