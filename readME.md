# Global Currency Strength Index (GCSI)

## DISCLAIMER

This project is for educational and analytical purposes only and does not constitute financial or investment advice.

--- 

## 1. Project Overview

**Global Currency Strength Index (GCSI)** is a Python-based macro-finance project that measures the relative strength of a chosen *base currency* against a basket of global currencies using transparent, index-style mathematics.

The project is designed as an improvement over traditional indices like the DXY by:

* Allowing **base-currency switching** (e.g., USD, MXN)
* Including **both developed and emerging market currencies**
* Using **clean, reproducible index construction methods**

The MVP focuses on correctness, clarity, and analytical usefulness rather than trading execution.

---

## 2. Problem Motivation

The US Dollar Index (DXY) is widely used but structurally limited:

* Only 6 currencies
* Heavy concentration in EUR
* No emerging markets (e.g., MXN, CNY)
* Fixed, outdated weights

As a result, DXY often fails to capture how the dollar (or any other currency) is performing against the *global* FX landscape.

GCSI addresses this gap by providing a flexible, base-agnostic currency strength framework.

---

## 3. MVP Scope

### Included in MVP

* Daily currency strength index
* User-selectable **base currency**
* Fixed **global currency universe**
* Index normalized to 100 at start date
* Equal-weighted and trade-weighted aggregation
* Comparison against DXY (USD-only benchmark)
* Time-series visualization

### Explicitly Out of Scope (MVP)

* Intraday data
* FX carry / interest rate effects
* Dynamic rebalancing
* Volatility targeting
* Trading signals or execution

---

## 4. Currency Universe (Fixed for MVP)

The MVP uses a predefined global basket designed to balance liquidity, regional coverage, and economic relevance.

| Currency | Region        | Country        | EM / DM |
| -------- | ------------- | -------------- | ------- |
| USD      | North America | United States  | DM      |
| CAD      | North America | Canada         | DM      |
| MXN      | North America | Mexico         | EM      |
| EUR      | Europe        | Euro Area      | DM      |
| GBP      | Europe        | United Kingdom | DM      |
| CHF      | Europe        | Switzerland    | DM      |
| JPY      | Asia          | Japan          | DM      |
| CNY      | Asia          | China          | EM      |
| KRW      | Asia          | South Korea    | EM      |
| AUD      | Asia-Pacific  | Australia      | DM      |
| BRL      | South America | Brazil         | EM      |


Currencies are freely traded and sufficiently liquid for daily analysis.

---

## 5. Base Currency Design

### Default Base Currency

* **USD (US Dollar)**

Rationale:

* Global reserve currency
* Natural benchmark vs DXY
* Most intuitive for users

### Supported Secondary Base (MVP)

* **MXN (Mexican Peso)**

Rationale:

* Illustrates base-currency switching
* Highlights emerging-market strength
* Enables alternative macro narratives

> Base currencies must be excluded from the comparison universe to avoid circularity.

---

## 6. Index Construction Methodology

### 6.1 FX Rate Normalization

All exchange rates are expressed relative to the chosen base currency.

If FX data is quoted as USD pairs:

* USD base: use rates directly
* Non-USD base: re-normalize using cross rates

This ensures mathematical consistency across base currencies.

---

### 6.2 Return Calculation

For each currency *i* at time *t*:

$`
r_{i,t} = ln(\frac{FX_{base/i,t}}{FX_{base/i,t−1}})
`$

Where: 
* $`r_{i,t}`$ is the log return of currency *i* at time *t*
* $`FX_{base/i,t}`$ is the exchange rate at time *t*
* $`FX_{base/i,t-1}`$ is the exchange rate at time *t-1*

Log returns are used for:

* Additivity
* Numerical stability
* Industry-standard index construction

---

### 6.3 Aggregation

Let weights $`w_i`$ satisfy:

$`
\sum{w_i} = 1
`$

Index return at time *t*:

$`
R{_t} = \sum{w_i} \cdot r{_i,t}
`$

The index return represents the weighted log return of the base currency against a basket of foreign currencies.
---


### 6.4 Index Level

The index is normalized to 100 at the start date:

$`
I{_t} = I_0 \cdot exp(\sum_{k=1} ^{t} R_k), I_0 = 100
`$

Interpretation:

* Index ↑ → base currency strengthening
* Index ↓ → base currency weakening

---


## 7. Data Sources

### Primary Source (MVP)

* **Yahoo Finance**

Examples:

* EURUSD=X
* USDJPY=X
* USDMXN=X

Rationale:

* Free and accessible
* Daily historical coverage
* Easy integration via Python

---

### Frequency

* Daily close prices

---

## 9. Outputs

### Visualizations

* Time-series plot of index level
* Percentage change since base date

### Tables

* Currency weights
* Contribution to index return

---

## 9. Benchmarks

* **DXY (US Dollar Index)** used as a reference benchmark for USD-based analysis
* **DTWEXBGS (Nominal Broad U.S. Dollar Index)** used as a reference benchmark for USD-based analysis

GCSI is positioned as a complementary and more globally representative alternative than DXY and similar to DTWEXBGS.

---

## 11. Project Structure (High-Level)

```
├── data/
│   └── fx_rates.csv
├── src/
│   ├── index.py
│   ├── data_loader.py
│   └── utils.py
├── app.py  # Streamlit MVP
├── README.md
└── requirements.txt
```

---

