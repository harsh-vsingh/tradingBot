from typing import Literal, Optional
from pydantic import BaseModel, Field, model_validator

OrderSide = Literal["BUY", "SELL"]
OrderType = Literal["MARKET", "LIMIT", "STOP_LIMIT"]


class OrderRequest(BaseModel):
    """
    A Pydantic model to represent and validate a new order request.
    """
    # Allow both 'stop_price' from the CLI and 'stopPrice' internally
    model_config = {"populate_by_name": True}

    symbol: str = Field(..., description="Trading symbol, e.g., BTCUSDT")
    side: OrderSide
    order_type: OrderType = Field(..., alias="type")
    quantity: float = Field(..., gt=0, description="Order quantity must be positive")
    price: Optional[float] = Field(None, gt=0, description="Required for LIMIT and STOP_LIMIT orders")
    
    # *** FIX IS HERE ***
    # We now accept 'stop_price' as an input alias from the CLI,
    # and use 'triggerPrice' as the output alias for the API.
    stopPrice: Optional[float] = Field(
        None,
        alias="stop_price", # Alias for input from CLI
        validation_alias="stop_price",
        serialization_alias="triggerPrice", # Alias for output to API
        gt=0,
        description="Required for STOP_LIMIT orders",
    )
    timeInForce: Optional[str] = None

    @model_validator(mode="after")
    def check_conditional_prices(self) -> "OrderRequest":
        if self.order_type == "LIMIT" and self.price is None:
            raise ValueError("Price is required for LIMIT orders.")
        if self.order_type == "STOP_LIMIT":
            if self.price is None:
                raise ValueError("Price is required for STOP_LIMIT orders.")
            if self.stopPrice is None:
                raise ValueError("stopPrice is required for STOP_LIMIT orders.")
        if self.order_type == "MARKET" and self.price is not None:
            self.price = None
        return self

    def to_api_params(self) -> dict:
        # `by_alias=True` now correctly uses 'triggerPrice' on output
        params = self.model_dump(by_alias=True, exclude_none=True)

        if params.get("type") == "STOP_LIMIT":
            params["type"] = "STOP"

        if params.get("type") in ["LIMIT", "STOP"] and "timeInForce" not in params:
            params["timeInForce"] = "GTC"

        return params