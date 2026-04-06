import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from currency_index.fx_data import DEFAULT_USD_BASKET, download_usd_base_fx_rates
from currency_index.index_builder import aggregate_returns, build_index
from currency_index.returns import compute_log_returns
from currency_index.weights import equal_weights, fixed_weights


@st.cache_data(ttl=3600)
def load_fx_data(currencies: list[str], start_date: date, end_date: date) -> pd.DataFrame:
    return download_usd_base_fx_rates(currencies, start_date, end_date)


def normalize_weights(currencies: list[str], custom_values: dict[str, float]) -> pd.Series:
    if not currencies:
        return pd.Series(dtype=float)

    series = pd.Series(custom_values, index=currencies, dtype=float)
    if series.sum() <= 0:
        return equal_weights(currencies)
    return fixed_weights(series.to_dict())


def main() -> None:
    st.set_page_config(page_title="Custom Dollar Index", layout="wide")
    st.title("Custom Dollar Index Dashboard")

    with st.sidebar:
        st.header("Index settings")
        start_default = date.today() - timedelta(days=365)
        start_date = st.date_input("Start date", value=start_default)
        end_date = st.date_input("End date", value=date.today())
        selected_currencies = st.multiselect(
            "Select currencies",
            options=DEFAULT_USD_BASKET,
            default=DEFAULT_USD_BASKET,
        )

        weight_mode = st.radio("Weight mode", ["Equal weights", "Custom weights"])
        custom_weights: dict[str, float] = {}
        if weight_mode == "Custom weights":
            st.markdown("Use the sliders below to set relative importance and normalize automatically.")
            for currency in selected_currencies:
                custom_weights[currency] = st.slider(
                    currency,
                    min_value=0.0,
                    max_value=1.0,
                    value=1.0 / max(len(selected_currencies), 1),
                    step=0.01,
                )

    if start_date >= end_date:
        st.error("End date must be after start date.")
        return

    if not selected_currencies:
        st.error("Please select at least one currency.")
        return

    try:
        fx_rates = load_fx_data(selected_currencies, start_date, end_date)
    except Exception as exc:
        st.error(f"Could not load FX data: {exc}")
        return

    log_returns = compute_log_returns(fx_rates).dropna()
    if log_returns.empty:
        st.warning("Not enough data for the selected date range.")
        return

    if weight_mode == "Equal weights":
        weights = equal_weights(selected_currencies)
    else:
        weights = normalize_weights(selected_currencies, custom_weights)

    index_returns = aggregate_returns(log_returns, weights)
    index_series = build_index(index_returns)
    index_series.name = "Dollar Index"

    st.sidebar.write("### Normalized weights")
    st.sidebar.dataframe(weights.rename("weight").to_frame())

    st.subheader("Index overview")
    last_index = index_series.iloc[-1]
    last_return = index_returns.iloc[-1] * 100
    col1, col2 = st.columns(2)
    col1.metric("Last index value", f"{last_index:.2f}")
    col2.metric("Most recent daily return", f"{last_return:.2f}%")

    st.line_chart(index_series)

    st.subheader("FX rates used for USD base")
    st.line_chart(fx_rates)

    st.subheader("Index return contribution")
    contribution = log_returns.multiply(weights, axis=1)
    contribution.columns = [f"{c} contribution" for c in contribution.columns]
    st.area_chart(contribution)

    st.markdown(
        "---\n"
        "*Data is downloaded from Yahoo Finance. Rates have been normalized so the dashboard reflects a USD base index.*"
    )


if __name__ == "__main__":
    main()
