# Trading Bot CLI

This project is a command-line interface (CLI) trading bot for interacting with the Binance Futures Testnet. It allows users to place `MARKET`, `LIMIT`, and `STOP_LIMIT` orders through a user-friendly interactive menu.

## Features

-   **Interactive CLI**: A menu-driven interface that prompts the user for order details one by one.
-   **Multiple Order Types**: Supports `MARKET`, `LIMIT`, and `STOP_LIMIT` orders.
-   **Input Validation**: Pre-validates all user inputs before sending requests to the API.
-   **Rich Formatting**: Uses the `rich` library for a clean, modern, and readable CLI experience with spinners, tables, and styled panels.
-   **Configuration Management**: Securely manages API keys using a `.env` file.
-   **Structured Logging**: Saves detailed logs of all placed orders to `trading_bot.log`.

## Setup Steps

### 1. Prerequisites

-   Python 3.12+
-   Git
-   `uv` (for environment and package management)

### 2. Clone the Repository

```bash
git clone https://github.com/harsh-vsingh/tradingBot.git
cd tradingBot
```

### 3. Create a Virtual Environment

Create and activate a virtual environment and install dependencies using `uv`.

```bash
uv sync
```

### 5. Configure API Keys

The application requires Binance Futures Testnet API keys.

a. **Get your keys** from the [Binance Futures Testnet](https://testnet.binancefuture.com/).

b. **Create a `.env` file** in the project's root directory
# .env
BINANCE__API_KEY="YOUR_API_KEY_HERE"
BINANCE__API_SECRET="YOUR_API_SECRET_HERE"
```

## How to Run

### Interactive Mode

This is the primary way to use the bot. It will guide you through placing an order with a series of prompts.

1.  **Run the command:**

    ```bash
    uv run python cli.py trade
    ```

2.  **Follow the prompts:** The application will ask for the symbol, order side, order type, quantity, and price as needed.


### Automated Script

A script is included to programmatically place one of each supported order type. This is useful for quickly testing functionality and generating logs.

```bash
uv run python place_all_orders.py
```

## Project Assumptions

-   **Testnet Only**: The bot is configured to work exclusively with the **Binance Futures Testnet**. It is not intended for use with a live production account.
-   **`uv` for Environment**: The setup instructions assume the use of `uv` for package and environment management.
-   **Manual Execution**: This is a manually triggered CLI tool, not a continuously running, autonomous trading bot.
-   **User Fund Management**: The user is responsible for ensuring they have sufficient funds in their testnet account to cover the orders they place.