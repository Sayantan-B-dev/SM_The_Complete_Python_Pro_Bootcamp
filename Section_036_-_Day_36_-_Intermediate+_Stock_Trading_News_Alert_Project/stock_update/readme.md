# Market Signal News & WhatsApp Alert System

---

## Project Overview

This project is a **command-line market monitoring system** that tracks significant **stock price movements**, enriches those movements with **relevant news context**, and optionally sends **WhatsApp alerts** when predefined conditions are met.
The system is intentionally **signal-driven**, meaning it avoids unnecessary API calls and notifications unless a meaningful market event occurs.

At a high level, the workflow follows this principle:

> *Numbers first, context second, notification last.*

---

## Core Capabilities

* Resolves human-friendly asset keywords into real market symbols
* Fetches daily market data from Alpha Vantage
* Calculates percentage price movement using the most recent trading sessions
* Conditionally fetches related news articles when movement is significant
* Renders structured, readable terminal output using Rich
* Sends rate-limited WhatsApp alerts via Twilio when thresholds are crossed

---

## Execution Flow Summary

```
User Command
   ↓
Asset Keyword Resolution
   ↓
Market Data Fetch (Alpha Vantage)
   ↓
Percentage Change Calculation
   ↓
Threshold Evaluation (> 5%)
   ↓
News Fetch (NewsAPI)
   ↓
Terminal Rendering
   ↓
Optional WhatsApp Alert (Cooldown Protected)
```

---

## Running the Application

### Default Execution (Apple Stock)

Running the application without any arguments defaults the monitored asset to **Apple (AAPL)**.

```bash
python main.py
```

This internally resolves to:

```
news_about=apple
```

---

### Custom Asset Execution

You can explicitly specify the asset keyword using the `news_about` argument.

```bash
python main.py news_about="tesla"
```

The keyword must match one of the supported asset identifiers defined in `assets.py`.
If an unsupported keyword is provided, the application will display a table of valid options.

---

## Environment Configuration (`.env`)

All credentials and external endpoints are loaded from a `.env` file located at the project root.
This ensures secrets are never hardcoded and can be rotated safely.

### Required `.env` Variables

```env
ALPHAVANTAGE_STOCK_ENDPOINT=https://www.alphavantage.co/query
NEWS_ENDPOINT=https://newsapi.org/v2/top-headlines

NEWS_API_KEY=**********
ALPHAVANTAGE_API_KEY=**********

TWILIO_ACCOUNT_SID=**********
TWILIO_AUTH_TOKEN=**********
TWILIO_WHATSAPP_NUMBER=**********
MY_PHONE_NUMBER=**********
```

---

## Environment Variable Responsibilities

### Market Data (Alpha Vantage)

* `ALPHAVANTAGE_STOCK_ENDPOINT`
  Base REST endpoint used for all market data requests.

* `ALPHAVANTAGE_API_KEY`
  Authenticates requests for daily stock, crypto, and forex time series data.

---

### News Data (NewsAPI)

* `NEWS_ENDPOINT`
  Endpoint used to fetch top headlines related to the monitored asset.

* `NEWS_API_KEY`
  Authenticates requests to the NewsAPI service.

---

### WhatsApp Alerts (Twilio)

* `TWILIO_ACCOUNT_SID`
  Identifies your Twilio account.

* `TWILIO_AUTH_TOKEN`
  Authenticates REST API requests to Twilio.

* `TWILIO_WHATSAPP_NUMBER`
  Twilio-provisioned WhatsApp sender number.

* `MY_PHONE_NUMBER`
  Destination WhatsApp number that receives alerts.

WhatsApp alerts are **optional**.
If any Twilio-related variable is missing, the alert subsystem fails safely without crashing the application.

---

## Notification Behavior and Safety Controls

* WhatsApp alerts are sent **only when price movement exceeds 5%**.
* Alerts are protected by a **12-hour cooldown**, persisted across runs using a lock file.
* Failed message attempts do not trigger cooldown activation.
* Missing credentials or network errors do not interrupt core program execution.

---

## Supported Asset Types

* Stocks (e.g., Apple, Tesla, Nvidia)
* Cryptocurrencies (e.g., Bitcoin, Ethereum)
* Forex pairs (e.g., USD/INR, EUR/USD)
* Market indices and ETFs (via mapped symbols)

The full list of supported keywords is displayed automatically when an invalid keyword is supplied.

---

## Design Philosophy

* **Deterministic execution**, no background state or daemons
* **Explicit API contract validation**, no blind parsing
* **Fail-safe behavior**, never crash on external service issues
* **Clear separation of concerns**, orchestration vs domain logic vs infrastructure
* **Human-readable output**, optimized for terminal usage

---

## Intended Usage

This tool is ideal for:

* Periodic execution via cron or task scheduler
* Lightweight market monitoring without dashboards
* Alerting only on meaningful volatility events
* Learning reference for API orchestration and defensive Python design

---

## Minimal Command Recap

```bash
python main.py
python main.py news_about="apple"
python main.py news_about="bitcoin"
```

The application exits cleanly after each run and maintains no long-lived processes.
