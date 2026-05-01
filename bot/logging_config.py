import logging
import sys

def setup_logging():
    """
    Configures structured logging to a file and to the console.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[
            logging.FileHandler("trading_bot.log"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    logging.getLogger("binance.websocket.websocket_client").setLevel(logging.WARNING)