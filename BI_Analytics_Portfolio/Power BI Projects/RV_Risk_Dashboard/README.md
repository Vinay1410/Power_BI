\# Residual Value Risk Performance Dashboard (Power BI)
## **All projects use simulated or public datasets via Python Code. No confidential/proprietary business data is included.**



\## Overview

This project demonstrates how I approach Residual Value (RV) Risk analytics in a captive auto finance environment using \*\*Power BI + Python-generated lease return data\*\*.  

The dashboard focuses on RV performance monitoring, risk drivers (mileage, model, body type), and regional market volatility — aligned to how RV risk teams monitor portfolio health and emerging loss exposure.


---



\## Key Outcomes \& Insights

\- \*\*Mileage is a structural risk driver:\*\* residual performance deteriorates significantly beyond ~60K mileage.

\- \*\*Portfolio trend visibility:\*\* gain/loss patterns show clear market shocks (spike years vs correction years).

\- \*\*Model \& body-type risk segmentation:\*\* identifies high-loss and high-volume exposures for pricing/forecasting discussions.

\- \*\*Regional risk monitoring:\*\* compares provinces using performance, volatility, loss ratio, and volume exposure.

\- \*\*Accurate geography design:\*\* implemented \*\*Latitude/Longitude\*\* to eliminate geocoding ambiguity and keep map plotting in Canada.



---



\## Dashboard Pages



\### 1) Intro / Navigation

Central navigation with global filters for consistent cross-page analysis.

\- Global slicers: \*\*Body Type\*\*, \*\*Province\*\*

\- Reset functionality: \*\*Clear filters button\*\*



📸 Screenshot: Visualizations/01_intro.png



---



\### 2) RV Portfolio Overview

Executive summary view of overall residual performance.

\- KPIs: Total Units, Avg Residual Value, Avg Sale Price, Avg Gain/Loss %, Total Gain/Loss $

\- Risk driver visualization: \*\*Mileage-banded bubble scatter\*\*

\- Time trend: Gain/Loss % by Lease End Year

\- Model trends: small multiple performance trends



📸 Screenshot: Visualizations/02_rv_portfolio_overview.png



---



\### 3) Model \& Body-Type Risk

Deep-dive into model and body type performance.

\- Model exposure segmentation

\- Model/year performance table

\- Body-type performance trends over time



📸 Screenshot: Visualizations/03_model_bodyType_risk.png



---



\### 4) Regional Risk \& Market Volatility

Risk monitoring view focused on province-level exposure and volatility.

\- KPIs: Avg Gain/Loss %, Total Gain/Loss $, Units with Loss, Loss Ratio %

\- Province \& body-type risk table with conditional formatting

\- Geographic exposure map using \*\*Lat/Long\*\*



📸 Screenshot: Visualizations/04_market_volatility.png



---



\## Dataset \& Assumptions



\### Dataset

\- ~220K lease return records (2013–2025)

\- Lease-level granularity (1 row per lease)

\- Key fields: Province, Model, Body Type, Residual Value, Actual Sale Price, Gain/Loss %, Mileage, Lease End Year.



\### Modeling assumptions (simulation logic)

\- Market cycles included:

&nbsp; - \*\*2020–2021 spike\*\* (strong used-car market)

&nbsp; - \*\*2022–2023 correction\*\* (normalization)

\- Sale price influenced by:

&nbsp; - Market index (year effect)

&nbsp; - Province factor (regional demand)

&nbsp; - Mileage penalty (usage impact)

&nbsp; - Noise term (realistic variability)



---



\## Tools \& Skills Demonstrated



\### Analytics \& Risk Thinking

\- Residual value performance monitoring

\- Market volatility analysis

\- Loss ratio and risk exposure tracking

\- Root-cause exploration (model/body type/mileage/province)



\### Power BI

\- Measures-driven reporting (DAX)

\- Slicer sync + cross-page filtering

\- Executive layout design and storytelling

\- Lat/Long mapping to avoid geocoding errors

\- Conditional formatting \& KPI design



\### Python (VS Code)

\- Generated simulated lease return dataset using a Python script executed in \*\*Visual Studio Code\*\*

\- Designed the dataset schema to remain consistent across refreshes to avoid breaking visuals



---



\## How to Run / Reproduce



\### 1) Generate dataset

Run the script:

```bash

python scripts/Generate_RV_Data.py



