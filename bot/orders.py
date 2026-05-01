import logging
from typing import Dict, Any

from binance.exceptions import BinanceAPIException, BinanceRequestException

from .client import get_binance_client
from .models import OrderRequest

logger = logging.getLogger(__name__)


def place_order(order_request: OrderRequest) -> Dict[str, Any]:
    """
    Places a futures order on Binance using a validated OrderRequest model.
    """
    client = get_binance_client()
    order_params = order_request.to_api_params()

    logger.info(f"Preparing to place order with params: {order_params}")

    try:
        if order_request.order_type in ["MARKET", "LIMIT"]:
            order_response = client.futures_create_order(**order_params)
        elif order_request.order_type == "STOP_LIMIT":
            order_response = client.futures_create_algo_order(**order_params)
        else:
            raise ValueError(f"Unsupported order type: {order_request.order_type}")

        logger.info(f"Successfully placed order. Response: {order_response}")
        return order_response
    except (BinanceAPIException, BinanceRequestException) as e:
        logger.error(f"Binance API/Request Error while placing order: {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise