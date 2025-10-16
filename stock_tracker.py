import yfinance as yf
import smtplib
from email.mime.text import MIMEText
import pandas as pd
import datetime

# Load tracked stocks
stocks = pd.read_csv("stocks.csv")  # Symbol, Target, Email

def send_email(subject, body, to_email):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "your_email@gmail.com"
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("your_email@gmail.com", "your_app_password")
        server.send_message(msg)

def check_prices():
    for _, row in stocks.iterrows():
        symbol = row["Symbol"]
        target = row["Target"]
        data = yf.Ticker(symbol).history(period="1d")
        price = data["Close"].iloc[-1]
        prev_close = data["Close"].iloc[-2]
        change = ((price - prev_close) / prev_close) * 100

        alert = None
        if price >= target:
            alert = f"🎯 {symbol} hit target {target}. Current: {price:.2f}"
        elif abs(change) > 3:
            alert = f"⚡ {symbol} moved {change:.2f}% today! Price: {price:.2f}"

        if alert:
            send_email(f"Stock Alert: {symbol}", alert, row["Email"])

    # Daily summary
    summary = "\n".join([f"{s} – {yf.Ticker(s).history(period='1d')['Close'].iloc[-1]:.2f}" for s in stocks["Symbol"]])
    send_email("Daily Stock Summary", summary, "aditya@example.com")

# check_prices()
print('I am here')

