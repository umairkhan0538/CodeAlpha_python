import json
import os
import requests
from datetime import datetime
from tabulate import tabulate
import matplotlib.pyplot as plt

# Alpha Vantage API key (replace with your own)
API_KEY = "YOUR_API_KEY"
BASE_URL = "https://www.alphavantage.co/query"

class PortfolioTracker:
    def __init__(self, portfolio_file="portfolio.json"):
        self.portfolio_file = portfolio_file
        self.portfolio = self.load_portfolio()

    def load_portfolio(self):
        """Load portfolio from JSON file or create a new one."""
        if os.path.exists(self.portfolio_file):
            with open(self.portfolio_file, 'r') as f:
                return json.load(f)
        return {"stocks": []}

    def save_portfolio(self):
        """Save portfolio to JSON file."""
        with open(self.portfolio_file, 'w') as f:
            json.dump(self.portfolio, f, indent=4)

    def get_stock_price(self, symbol):
        """Fetch current stock price from Alpha Vantage."""
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": API_KEY
        }
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            if "Global Quote" in data and "05. price" in data["Global Quote"]:
                return float(data["Global Quote"]["05. price"])
            else:
                error_msg = data.get("Note", "Unknown error") if "Note" in data else "Invalid symbol or missing data."
                print(f"Error fetching data for {symbol}: {error_msg}")
                return None
        except requests.RequestException as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None

    def add_stock(self, symbol, shares, purchase_price, purchase_date):
        """Add a stock to the portfolio."""
        symbol = symbol.upper()
        current_price = self.get_stock_price(symbol)
        if current_price is None:
            return

        stock = {
            "symbol": symbol,
            "shares": shares,
            "purchase_price": purchase_price,
            "purchase_date": purchase_date,
            "current_price": current_price
        }
        self.portfolio["stocks"].append(stock)
        self.save_portfolio()
        print(f"Added {shares} shares of {symbol} to portfolio.")

    def remove_stock(self, symbol):
        """Remove a stock from the portfolio."""
        symbol = symbol.upper()
        self.portfolio["stocks"] = [stock for stock in self.portfolio["stocks"] if stock["symbol"] != symbol]
        self.save_portfolio()
        print(f"Removed {symbol} from portfolio.")

    def update_prices(self):
        """Update current prices for all stocks in the portfolio."""
        for stock in self.portfolio["stocks"]:
            current_price = self.get_stock_price(stock["symbol"])
            if current_price is not None:
                stock["current_price"] = current_price
        self.save_portfolio()

    def view_portfolio(self):
        """Display portfolio with performance metrics."""
        if not self.portfolio["stocks"]:
            print("Portfolio is empty.")
            return

        self.update_prices()
        table = []
        total_value = 0
        total_invested = 0
        total_gain = 0

        for stock in self.portfolio["stocks"]:
            current_value = stock["shares"] * stock["current_price"]
            invested = stock["shares"] * stock["purchase_price"]
            gain = current_value - invested
            gain_percent = (gain / invested) * 100 if invested > 0 else 0

            table.append([
                stock["symbol"],
                stock["shares"],
                f"${stock['purchase_price']:.2f}",
                f"${stock['current_price']:.2f}",
                f"${current_value:.2f}",
                f"${gain:.2f}",
                f"{gain_percent:.2f}%"
            ])

            total_value += current_value
            total_invested += invested
            total_gain += gain

        headers = ["Symbol", "Shares", "Purchase Price", "Current Price", "Current Value", "Gain/Loss", "Gain/Loss %"]
        print("\nPortfolio Summary:")
        print(tabulate(table, headers, tablefmt="grid"))
        print(f"\nTotal Invested: ${total_invested:.2f}")
        print(f"Total Value: ${total_value:.2f}")
        print(f"Total Gain/Loss: ${total_gain:.2f} ({(total_gain/total_invested)*100:.2f}%)")

    def plot_performance(self):
        """Plot portfolio value over time (simplified, using current and purchase values)."""
        if not self.portfolio["stocks"]:
            print("Portfolio is empty.")
            return

        symbols = [stock["symbol"] for stock in self.portfolio["stocks"]]
        purchase_values = [stock["shares"] * stock["purchase_price"] for stock in self.portfolio["stocks"]]
        current_values = [stock["shares"] * stock["current_price"] for stock in self.portfolio["stocks"]]

        x = range(len(symbols))
        plt.figure(figsize=(10, 6))
        plt.bar(x, purchase_values, width=0.4, label="Purchase Value", color="blue")
        plt.bar([i + 0.4 for i in x], current_values, width=0.4, label="Current Value", color="green")
        plt.xticks([i + 0.2 for i in x], symbols)
        plt.xlabel("Stocks")
        plt.ylabel("Value ($)")
        plt.title("Portfolio Performance")
        plt.legend()
        plt.tight_layout()
        plt.savefig('portfolio_performance.png')
        print("Performance chart saved as 'portfolio_performance.png'")

def main():
    tracker = PortfolioTracker()
    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Portfolio")
        print("4. Plot Performance")
        print("5. Exit")
        try:
            choice = input("Enter choice (1-5): ")
        except EOFError:
            print("Input interrupted. Exiting...")
            break

        if choice == "1":
            try:
                symbol = input("Enter stock symbol (e.g., AAPL): ")
                shares = float(input("Enter number of shares: "))
                purchase_price = float(input("Enter purchase price per share: "))
                purchase_date = input("Enter purchase date (YYYY-MM-DD): ")
                tracker.add_stock(symbol, shares, purchase_price, purchase_date)
            except ValueError:
                print("Invalid input. Please enter numeric values for shares and price.")
            except EOFError:
                print("Input interrupted. Skipping...")
        elif choice == "2":
            try:
                symbol = input("Enter stock symbol to remove: ")
                tracker.remove_stock(symbol)
            except EOFError:
                print("Input interrupted. Skipping...")
        elif choice == "3":
            tracker.view_portfolio()
        elif choice == "4":
            tracker.plot_performance()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()