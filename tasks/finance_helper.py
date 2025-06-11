# File: tasks/finance_helper.py

import yfinance as yf
import schedule
import time
from .speaker import say_text

# A dictionary to hold our active price alerts
# Format: { 'ticker': {'target': 123.45, 'direction': 'above'/'below'} }
_price_alerts = {}

def get_current_price(ticker):
    """
    Fetches the current market price for a given stock or crypto ticker.
    
    Args:
        ticker (str): The stock symbol (e.g., "MSFT") or crypto ticker (e.g., "BTC-USD").
        
    Returns:
        str: The current price or an error message.
    """
    try:
        print(f"💰 Fetching current price for {ticker}...")
        stock = yf.Ticker(ticker)
        
        # 'regularMarketPrice' is a reliable field for the current price
        # We can also use 'currentPrice' or other fields as a fallback
        current_price = stock.info.get('regularMarketPrice') or stock.info.get('currentPrice')
        
        if current_price is None:
            # For some assets, we might need to look at recent history
            hist = stock.history(period="1d")
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
        
        if current_price:
            return f"The current price of {ticker.upper()} is ${current_price:,.2f}."
        else:
            return f"Sorry, I couldn't find a current price for {ticker}. It might be an invalid ticker."
            
    except Exception as e:
        return f"Sorry, I encountered an error while fetching the price for {ticker}. Error: {e}"

def _check_price_alerts():
    """
    This function runs periodically in the background to check all active alerts.
    It is called by the main scheduler thread.
    """
    # We iterate over a copy of the items to allow safe modification during the loop
    for ticker, alert_info in list(_price_alerts.items()):
        try:
            stock = yf.Ticker(ticker)
            current_price = stock.info.get('regularMarketPrice') or stock.info.get('currentPrice')
            if not current_price: continue # Skip if we can't get a price
            
            target = alert_info['target']
            direction = alert_info['direction']
            
            print(f"DEBUG: Checking alert for {ticker}. Current: ${current_price}, Target: {direction} ${target}")

            # Check if the alert condition is met
            if (direction == 'above' and current_price > target) or \
               (direction == 'below' and current_price < target):
                
                alert_message = f"Price alert for {ticker.upper()}! It has gone {direction} your target of ${target:,.2f} and is now at ${current_price:,.2f}."
                print(f"🎯 PRICE ALERT: {alert_message}")
                say_text(alert_message)
                
                # Remove the alert after it has been triggered
                del _price_alerts[ticker]
                print(f"INFO: Alert for {ticker} has been triggered and removed.")
                
        except Exception as e:
            # Don't crash the checker thread, just log the error
            print(f"ERROR: Could not check price alert for {ticker}. Reason: {e}")


def set_price_alert(ticker, direction, target_price):
    """
    Sets a new price alert for a given ticker.
    
    Args:
        ticker (str): The stock or crypto ticker.
        direction (str): "above" or "below".
        target_price (float): The target price.
        
    Returns:
        str: A confirmation message.
    """
    if direction.lower() not in ['above', 'below']:
        return "Invalid direction. Please specify 'above' or 'below'."
        
    try:
        target = float(target_price)
        _price_alerts[ticker.upper()] = {'target': target, 'direction': direction.lower()}
        
        # If this is the first alert, we schedule the checker function to run.
        # It will run every 5 minutes.
        if len(schedule.get_jobs('price-checker')) == 0:
            schedule.every(5).minutes.do(_check_price_alerts).tag('price-checker')
            print("INFO: Started the periodic price alert checker (runs every 5 minutes).")
            
        confirmation = f"I will alert you if {ticker.upper()} goes {direction} ${target:,.2f}."
        print(f"✅ Alert set: {confirmation}")
        return f"Okay, alert set. {confirmation}"
        
    except ValueError:
        return f"Invalid target price '{target_price}'. Please provide a number."
    except Exception as e:
        return f"Sorry, I couldn't set the alert. Error: {e}"

def get_active_alerts():
    """Returns a list of all currently active price alerts."""
    if not _price_alerts:
        return "You have no active price alerts."
        
    alert_list = "Here are your active alerts:\n"
    for ticker, info in _price_alerts.items():
        alert_list += f"- {ticker}: Alert if price goes {info['direction']} ${info['target']:,}\n"
        
    return alert_list.strip()