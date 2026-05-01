from binance import Client
from .settings import settings

FUTURES_TESTNET_URL = "https://testnet.binancefuture.com"


def get_binance_client() -> Client:
    """
    Initializes and returns a Binance client configured for the Futures Testnet.
    """
    client = Client(
        api_key=settings.api_key,
        api_secret=settings.api_secret,
        testnet=True, 
    )
    client.API_URL = FUTURES_TESTNET_URL
    return client