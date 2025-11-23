from typing import List
from ddgs import DDGS  


def ddg_search_snippets(query: str, max_results: int = 5) -> List[str]:
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            title = r.get("title", "")
            snippet = r.get("body", "")
            url = r.get("href", "")
            results.append(f"Title: {title}\nURL: {url}\nSnippet: {snippet}")
    return results


def ddg_company_research(company: str, extra: str = "") -> str:
    q = f"{company} {extra}" if extra else company
    results = ddg_search_snippets(q, max_results=8)
    if not results:
        return "No results found."
    return "\n\n---\n\n".join(results)
