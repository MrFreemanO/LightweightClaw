import aiohttp
import logging
import psutil
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

async def crypto_price(symbol="BTC", **kwargs):
    """Get real cryptocurrency price via CoinGecko (Free API)"""
    try:
        async with aiohttp.ClientSession() as s:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol.lower()}&vs_currencies=usd"
            async with s.get(url) as r:
                data = await r.json()
                price = data.get(symbol.lower(), {}).get("usd")
                return price if price else f"Could not find coin {symbol}"
    except Exception as e:
        return f"CoinGecko API Error: {e}"

async def web_search(query, **kwargs):
    """Real web search parsing via DuckDuckGo (HTML) without API keys."""
    try:
        url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        for a in soup.find_all('a', class_='result__snippet')[:3]:
            results.append(a.text)
            
        return "\n\n".join(results) if results else "Search returned no results."
    except Exception as e:
        return f"Web search execution error: {str(e)}"

async def system_info(**kwargs):
    """Real host system data."""
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.5),
        "ram_percent": psutil.virtual_memory().percent,
        "disk_free_gb": round(psutil.disk_usage('/').free / (1024**3), 2)
    }

TOOL_REGISTRY = {
        "crypto_price": crypto_price,
        "web_search": web_search,
        "system_info": system_info
}
