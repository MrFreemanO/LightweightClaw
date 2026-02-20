import aiohttp
import logging
import psutil
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

async def crypto_price(symbol="BTC", **kwargs):
    """Получение реальной цены криптовалюты через CoinGecko (Free API)"""
    try:
        async with aiohttp.ClientSession() as s:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol.lower()}&vs_currencies=usd"
            async with s.get(url) as r:
                data = await r.json()
                price = data.get(symbol.lower(), {}).get("usd")
                return price if price else f"Не удалось найти монету {symbol}"
    except Exception as e:
        return f"Ошибка API CoinGecko: {e}"

async def memecoin_sniper(target_platform="pump.fun", dry_run=True, **kwargs):
    """
    Поиск новых мемкоинов (Интеграция с DexScreener API для Solana).
    ⚠️ ВНИМАНИЕ: ДЛЯ РЕАЛЬНОЙ ТОРГОВЛИ НЕОБХОДИМ ПРИВАТНЫЙ КЛЮЧ КОШЕЛЬКА!
    ВСТАВЛЯЙТЕ ЕГО ТОЛЬКО В LOKAL .env ФАЙЛ, НИКОГДА НЕ ПУШЬТЕ В GITHUB!
    """
    logger.info(f"Снайпер запущен: {target_platform} (Dry Run: {dry_run})")
    
    # ПРИМЕР РЕАЛЬНОГО ЗАПРОСА К ПУБЛИЧНОМУ API
    try:
        async with aiohttp.ClientSession() as s:
            # Ищем свежие пары на Solana
            async with s.get("https://api.dexscreener.com/latest/dex/search?q=solana") as r:
                data = await r.json()
                pairs = data.get("pairs", [])[:3]  # Берем топ-3 свежих
                targets = [f"{p.get('baseToken', {}).get('symbol', 'UNK')} (Liquidity: ${p.get('liquidity', {}).get('usd', 0)})" for p in pairs]
    except Exception as e:
        targets = [f"Ошибка парсинга DEX: {str(e)}"]

    return {
        "status": "dry_run_active" if dry_run else "⚠️ LIVE_TRADING_LOCKED (Требуется имплементация подписи транзакций в core/tools.py)",
        "targets": targets,
        "message": "Система снайпинга: данные получены с реального рынка (DexScreener)."
    }

async def web_search(query, **kwargs):
    """Реальный парсинг поисковой выдачи DuckDuckGo (HTML) без API ключей."""
    try:
        url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        for a in soup.find_all('a', class_='result__snippet')[:3]:  # Топ 3 результата
            results.append(a.text)
            
        return "\n\n".join(results) if results else "Поиск не дал результатов."
    except Exception as e:
        return f"Ошибка выполнения веб-поиска: {str(e)}"

async def system_info(**kwargs):
    """Реальные данные о системе хоста, на котором запущен агент."""
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.5),
        "ram_percent": psutil.virtual_memory().percent,
        "disk_free_gb": round(psutil.disk_usage('/').free / (1024**3), 2)
    }

TOOL_REGISTRY = {
    "crypto_price": crypto_price,
    "memecoin_sniper": memecoin_sniper,
    "web_search": web_search,
    "system_info": system_info
}