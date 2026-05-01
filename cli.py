import logging

import questionary
import typer
from pydantic import ValidationError
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from bot.logging_config import setup_logging
from bot.models import OrderRequest
from bot.orders import place_order
from bot.validators import is_valid_symbol

app = typer.Typer(
    name="Trading Bot",
    help="A simple CLI trading bot for Binance Futures Testnet.",
    add_completion=False,
)
console = Console()

logger = logging.getLogger(__name__)


@app.command()
def trade():
    """
    Interactively place a trade on the Binance Futures Testnet.
    """
    console.print(
        Panel(
            "[bold yellow]Welcome to the Interactive Trading Bot![/bold yellow]\n"
            "You will be prompted for order details.",
            title="[cyan]Interactive Mode[/cyan]",
            expand=False,
        )
    )

    try:
        symbol = questionary.text(
            "Enter the trading symbol (e.g., BTCUSDT):",
            validate=lambda text: True if text else "Symbol cannot be empty.",
        ).ask().upper()

        with console.status(f"[bold cyan]Validating symbol '{symbol}'...[/bold cyan]"):
            if not is_valid_symbol(symbol):
                console.print(f"[bold red]Error: Symbol '{symbol}' is not a valid futures symbol.[/bold red]")
                raise typer.Exit(code=1)
        console.print(f"✔ [green]Symbol '{symbol}' is valid.[/green]\n")

        side = questionary.select("Select order side:", choices=["BUY", "SELL"]).ask()
        order_type = questionary.select(
            "Select order type:", choices=["MARKET", "LIMIT", "STOP_LIMIT"]
        ).ask()

        quantity = questionary.text(
            "Enter quantity:",
            validate=lambda text: True
            if text and float(text) > 0
            else "Please enter a valid positive number.",
            ).ask()
        quantity = float(quantity)

        price = None
        if order_type in ["LIMIT", "STOP_LIMIT"]:
            price = questionary.text(
                f"Enter price for {order_type} order:",
                validate=lambda text: True
                if text and float(text) > 0
                else "Please enter a valid positive number.",
            ).ask()
            price = float(price)

        stop_price = None
        if order_type == "STOP_LIMIT":
            stop_price = questionary.text(
                "Enter stop price:",
                validate=lambda text: True
                if text and float(text) > 0
                else "Please enter a valid positive number.",
            ).ask()
            stop_price = float(stop_price)

        order_request = OrderRequest(
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price,
        )

    except (ValidationError, TypeError, AttributeError) as e:
        error_messages = "\n".join([f"- {err['msg']}" for err in getattr(e, 'errors', [])()])
        error_panel = Panel(
            f"[bold]The following order parameters are invalid:[/bold]\n\n{error_messages or str(e)}",
            title="[bold red]Validation Error[/bold red]",
            border_style="red",
            expand=False,
        )
        console.print(error_panel)
        raise typer.Exit(code=1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
        raise typer.Exit()


    summary_table = Table(title="[bold yellow]Order Request Summary[/bold yellow]", show_header=False)
    summary_table.add_column("Parameter", style="cyan")
    summary_table.add_column("Value", style="magenta")

    api_params = order_request.to_api_params()
    for key, value in api_params.items():
        summary_table.add_row(key.replace("_", " ").capitalize(), str(value))

    notional_value = (price or 0) * quantity if price else quantity
    if order_type == "MARKET":
        summary_table.add_row("[bold]Notional Value[/bold]", f"~{notional_value:.4f} USDT (Market Price)")
    else:
        summary_table.add_row("[bold]Notional Value[/bold]", f"{notional_value:.4f} USDT")

    console.print(summary_table)

    confirmed = questionary.confirm("Do you want to proceed and place this order?").ask()
    if not confirmed:
        console.print("[yellow]Order cancelled by user.[/yellow]")
        raise typer.Exit()

    try:
        with console.status("[bold cyan]Placing order...[/bold cyan]"):
            order_response = place_order(order_request)
        
        console.print("[bold green]✔ Order placed successfully![/bold green]")
        response_table = Table(title="[bold green]Order Response[/bold green]")
        response_table.add_column("Key", style="cyan")
        response_table.add_column("Value", style="magenta")
        for key, value in order_response.items():
            response_table.add_row(key, str(value))
        console.print(response_table)

    except Exception as e:
        error_panel = Panel(
            f"[bold]Failed to place order.[/bold]\n\n[white]Details: {e}[/white]",
            title="[bold red]API Error[/bold red]",
            border_style="red",
            expand=False,
        )
        console.print(error_panel)
        raise typer.Exit(code=1)


@app.callback()
def main():
    """
    Main callback to set up logging before any command runs.
    """
    setup_logging()


if __name__ == "__main__":
    app()