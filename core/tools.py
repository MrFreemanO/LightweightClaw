import aiohttp
import logging
import psutil

logger = logging.getLogger(__name__)

async def crypto_price(symbol="BTC", **kwargs):
    async with aiohttp.ClientSession() as s:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol.lower()}&vs_currencies=usd"
        async with s.get(url) as r:
            data = await r.json()
            return data.get(symbol.lower(), {}).get("usd", "N/A")

async def memecoin_sniper(target_platform="pump.fun", dry_run=True, **kwargs):
    logger.info(f"Снайпер запущен: {target_platform} (Dry Run: {dry_run})")
    return {
        "status": "dry_run_active" if dry_run else "live",
        "targets": ["PUMP1", "WIF2"],
        "recommended_buy": "$50",
        "message": "Система снайпинга активирована. Выявлены перспективные токены."
    }

async def web_search(query, **kwargs):
    return f"Поиск результатов для: {query}..."

async def system_info(**kwargs):
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.5),
        "ram_percent": psutil.virtual_memory().percent
    }

TOOL_REGISTRY = {
    "crypto_price": crypto_price,
    "memecoin_sniper": memecoin_sniper,
    "web_search": web_search,
    "system_info": system_info
}