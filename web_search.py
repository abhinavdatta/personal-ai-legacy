from duckduckgo_search import DDGS

def web_search(query: str, max_results: int = 3) -> list:
    """
    Performs a DuckDuckGo web search and returns
    short, clean text snippets.
    """
    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title": r.get("title"),
                "snippet": r.get("body"),
                "url": r.get("href")
            })

    return results
