import tkinter as tk
from tkinter import ttk
import requests

# API endpoint and key
API_URL = "https://api.freecurrencyapi.com/v1/latest"
API_KEY = "fca_live_vOH1Ag52u2v6Uij1UTZ3TqwsZfQQoMTFeqyMtryC"

# Major currencies to display
MAJOR_CURRENCIES = ["USD", "EUR", "GBP", "INR", "MYR", "IDR"]
MAJOR_CURRENCIES_LIST = ["EUR", "GBP", "INR", "MYR", "IDR"]

# Function to fetch live exchange rates
def fetch_rates():
    try:
        response = requests.get(f"{API_URL}?apikey={API_KEY}")
        data = response.json()
        rates = data.get("data", {})
        
        # Update exchange rates display
        rates_text = "\n".join([f"1 USD = {rates[currency]:.2f} {currency}" for currency in MAJOR_CURRENCIES_LIST if currency in rates])
        live_rates_label.config(text=rates_text)
        return rates
    except Exception as e:
        live_rates_label.config(text="Error fetching rates.")
        return {}

# Function to convert currency
def convert_currency():
    amount = amount_entry.get()
    from_currency = from_currency_combo.get()
    to_currency = to_currency_combo.get()

    # Validate input
    if not amount.replace(".", "").isdigit():
        result_label.config(text="Enter a valid amount.")
        return

    amount = float(amount)
    if from_currency == to_currency:
        result_label.config(text="Source and target currencies are the same.")
        return

    # Perform conversion
    from_rate = live_rates.get(from_currency, 1.0)
    to_rate = live_rates.get(to_currency, 1.0)
    converted_amount = amount * (to_rate / from_rate)
    result_label.config(text=f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")

# Function to switch "From" and "To" currencies
def switch_currencies():
    from_currency = from_currency_combo.get()
    to_currency = to_currency_combo.get()
    from_currency_combo.set(to_currency)
    to_currency_combo.set(from_currency)

# GUI setup
root = tk.Tk()
root.title("Live Currency Converter")
root.geometry("500x500")

# Live rates display
tk.Label(root, text="Live Exchange Rates", font=("Helvetica", 14, "bold")).pack(pady=10)
live_rates_label = tk.Label(root, text="", font=("Helvetica", 12), justify="left")
live_rates_label.pack(pady=5)

# Fetch live rates after label is defined
live_rates = fetch_rates()

# Amount input
tk.Label(root, text="Amount:").pack(pady=5)
amount_entry = tk.Entry(root, width=20)
amount_entry.pack(pady=5)

# Source currency
tk.Label(root, text="From Currency:").pack(pady=5)
from_currency_combo = ttk.Combobox(root, values=MAJOR_CURRENCIES, state="readonly", width=20)
from_currency_combo.set("USD")
from_currency_combo.pack(pady=5)

# Target currency
tk.Label(root, text="To Currency:").pack(pady=5)
to_currency_combo = ttk.Combobox(root, values=MAJOR_CURRENCIES, state="readonly", width=20)
to_currency_combo.set("INR")
to_currency_combo.pack(pady=5)

# Switch button
switch_button = tk.Button(root, text="Switch", command=switch_currencies, bg="lightblue")
switch_button.pack(pady=5)

# Convert button
convert_button = tk.Button(root, text="Convert", command=convert_currency)
convert_button.pack(pady=10)

# Result display
result_label = tk.Label(root, text="", font=("Helvetica", 12))
result_label.pack(pady=10)

# Copyright label placed at the bottom-right
copyright_label = tk.Label(
    root, 
    text="By Jeeteendar", 
    font=("Helvetica", 6, "italic"), 
    justify="right"
)
copyright_label.place(relx=1.0, rely=1.0, anchor="se")  # Bottom-right corner

root.mainloop()
