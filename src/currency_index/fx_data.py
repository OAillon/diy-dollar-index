import pandas as pd
import yfinance as yf
from datetime import date

USD_BASE_TICKERS: dict[str, tuple[str, bool]] = {
    "EUR": ("EURUSD=X", True),
    "GBP": ("GBPUSD=X", True),
    "AUD": ("AUDUSD=X", True),
    "JPY": ("USDJPY=X", False),
    "CAD": ("USDCAD=X", False),
    "CHF": ("USDCHF=X", False),
    "MXN": ("USDMXN=X", False),
    "CNY": ("USDCNH=X", False),
    "KRW": ("USDKRW=X", False),
}

DEFAULT_USD_BASKET: list[str] = ["EUR", "JPY", "GBP", "CAD", "CHF", "AUD", "MXN"]


def download_usd_base_fx_rates(
    currencies: list[str],
    start_date: date,
    end_date: date,
) -> pd.DataFrame:
    """Download FX rates expressed with USD as the base currency."""
    series_map: dict[str, pd.Series] = {}

    for currency in currencies:
        if currency not in USD_BASE_TICKERS:
            raise ValueError(f"Unsupported currency: {currency}")

        ticker, invert = USD_BASE_TICKERS[currency]
        raw = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            progress=False,
            actions=False,
        )

        if raw.empty:
            raise RuntimeError(f"No data returned for ticker {ticker}")

        close_data = raw["Close"]
        if isinstance(close_data, pd.DataFrame):
            data_series = close_data.iloc[:, 0].copy()
        else:
            data_series = close_data.copy()

        data_series.name = currency
        if invert:
            data_series = 1.0 / data_series

        series_map[currency] = data_series

    fx_rates = pd.DataFrame(series_map).sort_index(axis=1)
    return fx_rates
