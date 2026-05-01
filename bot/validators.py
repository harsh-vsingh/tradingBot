import logging
from typing import Set
from functools import lru_cache
from binance.exceptions import BinanceAPIException
from .client import get_binance_client

logger = logging.getLogger(__name__)

@lru_cache(maxsize=1)
def get_valid_symbols() -> Set[str]:
    """
    Fetches all valid trading symbols from the Binance Futures exchange.
    Results are cached to avoid repeated API calls.
    """
    logger.info("Fetching valid symbols from Binance...")
    client = get_binance_client()
    try:
        exchange_info = client.futures_exchange_info()
        symbols = {s["symbol"] for s in exchange_info["symbols"]}
        logger.info(f"Successfully fetched {len(symbols)} symbols.")
        return symbols
    except BinanceAPIException as e:
        logger.error(f"Failed to fetch exchange info: {e}")
        return set()

def is_valid_symbol(symbol: str) -> bool:
    """
    Checks if a given symbol is valid on the Binance Futures exchange.
    """
    return symbol.upper() in get_valid_symbols()