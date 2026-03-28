# Rental Price Forecast — Madrid Airbnb Time Series

Time series analysis and forecasting of Madrid's short-term rental market using **15 years of review data** (2010–2025) from Inside Airbnb.

---

## Goal

Analyse the temporal evolution of market demand and pricing in Madrid, and forecast future trends using classical and modern forecasting methods.

## Project structure

```
rental-price-forecast/
├── data/
│   └── raw/
│       ├── listings.csv.gz    ← Inside Airbnb listings snapshot
│       └── reviews.csv.gz     ← 15 years of review timestamps
├── notebooks/
│   └── 03_rental_price_forecast.ipynb
├── src/
│   └── utils.py
├── outputs/
│   └── figures/
├── requirements.txt
└── README.md
```

---

## Methodology

Reviews are used as a **proxy for bookings** (each review typically follows a stay). Joined with listing prices, they provide a monthly time series of both demand and price spanning over a decade.

| Step | Description |
|------|-------------|
| 1 | Join reviews × listings to get monthly demand + price |
| 2 | Exploratory analysis: trend, seasonality, YoY growth |
| 3 | Seasonal decomposition (additive, period=12) |
| 4 | SARIMA(1,1,1)(1,1,1,12) — statistical forecasting |
| 5 | Prophet — additive model with multiplicative seasonality |

---

## Models compared

| Model | Strengths |
|-------|-----------|
| SARIMA | Handles non-stationarity and seasonal differencing explicitly |
| Prophet | Robust to missing data, handles trend changes automatically |

---

## Installation & usage

```bash
git clone https://github.com/Abadalina/rental-price-forecast.git
cd rental-price-forecast
pip install -r requirements.txt
jupyter notebook notebooks/03_rental_price_forecast.ipynb
```

---

## Tech stack

![Python](https://img.shields.io/badge/Python-3.11-blue)
![statsmodels](https://img.shields.io/badge/statsmodels-0.14-4C72B0)
![Prophet](https://img.shields.io/badge/Prophet-1.1-0072C6)
![Pandas](https://img.shields.io/badge/Pandas-2.2-150458)

---

## Part of the Madrid Housing Portfolio

| # | Project | Description |
|---|---------|-------------|
| 1 | [spain-rental-eda](https://github.com/Abadalina/spain-rental-eda) | Exploratory data analysis |
| 2 | [housing-price-ml](https://github.com/Abadalina/housing-price-ml) | ML price prediction |
| 3 | **rental-price-forecast** | Time series forecasting ← you are here |
| 4 | [airbnb-reviews-nlp](https://github.com/Abadalina/airbnb-reviews-nlp) | NLP sentiment & topic analysis |
| 5 | [housing-price-app](https://github.com/Abadalina/housing-price-app) | Streamlit deployment |
| 6 | [spain-airbnb-dashboard](https://github.com/Abadalina/spain-airbnb-dashboard) | Live market dashboard |

---

## Author

**Alejandro Abadal** — Data Science Student, UOC
[LinkedIn](#) · [GitHub](https://github.com/Abadalina)

---

*Data for educational purposes. Source: Inside Airbnb.*
