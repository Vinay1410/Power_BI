Insurance & Benefits KPI Demo Dataset (Simulated RAW + Governed fields)

Purpose:
- A generic, fictional dataset designed to demonstrate how a Senior BI / Data & Analytics Analyst can
  build a governed “single source of truth” model and KPI dashboards for an insurer / group benefits provider.

Included tables (CSV):
Dimensions:
- DimDate.csv
- DimClient.csv
- DimAdvisor.csv
- DimEmployer.csv
- DimProduct.csv
- DimProvider.csv

Facts:
- FactPolicy.csv
- FactTransactions.csv
- FactClaims.csv
- FactServiceRequests.csv
- FactDataQualityMonthly.csv

Intentional realism / “messiness”:
- DimClient_original_with_messy_province.csv shows typical source-system issues (mixed codes/names/spaces).
- DimClient.csv is standardized to province codes + Unknown to represent a curated/gold layer.
- Small % missing AdvisorID in FactTransactions (to show referential integrity handling).
- Small % missing ProviderID in FactClaims.

Use case ideas:
- Executive KPIs (premiums, claims paid, loss ratio, SLA, CSAT, data quality)
- Claims ops monitoring (TAT, denial reasons, provider hotspots)
- Advisor/channel performance (volume, persistency proxies, service burden)
- Data governance scorecards (completeness/uniqueness/consistency trends)
