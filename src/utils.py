"""
Helper functions for the rental price forecasting project.
Author: Alejandro Abadal
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import warnings

warnings.filterwarnings("ignore")

PALETTE = ["#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51"]
PRIMARY  = "#2a9d8f"
ACCENT   = "#e76f51"


def set_style():
    import seaborn as sns
    sns.set_theme(style="whitegrid", palette=PALETTE)
    plt.rcParams.update({
        "figure.facecolor": "#fafafa",
        "axes.facecolor":   "#fafafa",
        "axes.spines.top":  False,
        "axes.spines.right":False,
        "axes.titlesize":   14,
        "axes.titleweight": "bold",
        "axes.labelsize":   11,
    })


def clean_price(series: pd.Series) -> pd.Series:
    return (
        series.astype(str)
        .str.replace(r"[\$,]", "", regex=True)
        .str.strip()
        .replace("", np.nan)
        .astype(float)
    )


def load_listings(path: str) -> pd.DataFrame:
    cols = ['id', 'neighbourhood_cleansed', 'room_type', 'price',
            'review_scores_rating', 'number_of_reviews']
    df = pd.read_csv(path, low_memory=False, usecols=lambda c: c in cols)
    if not pd.api.types.is_numeric_dtype(df['price']):
        df['price'] = clean_price(df['price'])
    df = df.dropna(subset=['price'])
    df = df[df['price'] > 0]
    q_low, q_high = df['price'].quantile(0.01), df['price'].quantile(0.99)
    df = df[df['price'].between(q_low, q_high)]
    return df.reset_index(drop=True)


def load_reviews(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False,
                     usecols=['listing_id', 'date'],
                     parse_dates=['date'])
    df = df.dropna(subset=['date'])
    return df.reset_index(drop=True)


def build_monthly_ts(reviews: pd.DataFrame, listings: pd.DataFrame) -> pd.DataFrame:
    """
    Join reviews with listing prices and aggregate by month.
    Returns monthly series: review_count (demand proxy) + median_price.
    """
    merged = reviews.merge(listings[['id', 'price']],
                           left_on='listing_id', right_on='id', how='inner')
    merged['month'] = merged['date'].dt.to_period('M').dt.start_time

    monthly = (
        merged.groupby('month')
        .agg(
            review_count=('listing_id', 'count'),
            median_price=('price', 'median'),
            mean_price=('price', 'mean'),
        )
        .reset_index()
        .sort_values('month')
    )
    # Remove incomplete first/last months and pre-2012 sparse data
    monthly = monthly[monthly['month'] >= '2012-01-01']
    monthly = monthly[monthly['month'] < monthly['month'].max()]
    return monthly


def fmt_euro(x, pos=None):
    return f"{x:,.0f} €"


def save_fig(fig, name: str, dpi: int = 150):
    import os
    os.makedirs("../outputs/figures", exist_ok=True)
    path = f"../outputs/figures/{name}.png"
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    print(f"  Saved → {path}")
