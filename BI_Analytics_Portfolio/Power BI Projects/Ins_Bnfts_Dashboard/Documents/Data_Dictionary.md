# 📘 **Data Dictionary**
Enterprise Benefits Performance & Risk Dashboard  

> ⚠️ All data in this project is synthetically generated using Python for demonstration purposes. No real client or employer data is included.

---

# 🧱 **Data Model Overview**

The data model follows a **Star Schema** design with:

- Dimension Tables (descriptive attributes)
- Fact Tables (transactional and performance metrics)

---

# 📊 **Fact Tables**

---

## 1️⃣ **FACT_Policy**

Represents policy-level premium activity.

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| PolicyID | Integer | Unique identifier for each policy |
| EmployerID | Integer (FK) | Links to DIM_Employer |
| ProductID | Integer (FK) | Links to DIM_Product |
| ClientID | Integer (FK) | Links to DIM_Client |
| AdvisorID | Integer (FK) | Links to DIM_Advisor |
| DateKey | Date (FK) | Links to DIM_Date |
| PremiumAmount | Decimal | Premium billed for the policy |
| SumAssured | Decimal | Coverage amount for the policy |
| PolicyStatus | Text | Active, Cancelled, Expired |

---

## 2️⃣ **FACT_Claims**

Contains claims-level financial and operational data.

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| ClaimID | Integer | Unique claim identifier |
| PolicyID | Integer (FK) | Links to FACT_Policy |
| EmployerID | Integer (FK) | Links to DIM_Employer |
| ProductID | Integer (FK) | Links to DIM_Product |
| ProviderID | Integer (FK) | Links to DIM_Provider |
| DateKey | Date (FK) | Claim incurred date |
| ClaimAmount | Decimal | Total claim value |
| PaidAmount | Decimal | Amount paid |
| ClaimStatus | Text | Open, Closed, Denied |
| HighSeverityFlag | Boolean | Indicates high-cost claim |
| ProcessingDays | Integer | Days taken to process claim |

---

## 3️⃣ **FACT_Transactions**

Aggregated monthly financial performance table.

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| DateKey | Date (FK) | Reporting month |
| EmployerID | Integer (FK) | Links to DIM_Employer |
| ProductID | Integer (FK) | Links to DIM_Product |
| PremiumsCollected | Decimal | Total premiums received |
| ClaimsPaid | Decimal | Total claims paid |
| NetMargin | Decimal | Premiums - Claims |
| LossRatio | Decimal | ClaimsPaid / PremiumsCollected |

---

## 4️⃣ **FACT_ServiceRequests**

Tracks operational service metrics.

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| RequestID | Integer | Unique service request ID |
| EmployerID | Integer (FK) | Links to DIM_Employer |
| DateKey | Date (FK) | Request date |
| ResolutionDays | Integer | Days to resolve issue |
| SLAFlag | Boolean | Whether SLA was met |
| CSATScore | Decimal | Customer satisfaction score |

---

## 5️⃣ **FACT_DataQualityMonthly**

Aggregated data quality scoring table.

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| DateKey | Date (FK) | Reporting month |
| RecordsChecked | Integer | Total records validated |
| TotalIssues | Integer | Number of detected data issues |
| DQScore | Decimal | Data quality score (%) |

---

# 📂 **Dimension Tables**

---

## **DIM_Date**

| Column Name | Description |
|-------------|-------------|
| DateKey | Primary key date |
| Year | Calendar year |
| Month | Month name |
| MonthNumber | Month numeric |
| YearMonth | YYYY-MM format |
| Quarter | Q1–Q4 |

---

## **DIM_Employer**

| Column Name | Description |
|-------------|-------------|
| EmployerID | Unique employer ID |
| EmployerName | Employer name |
| Industry | Industry classification |
| Province | Canadian province |
| EmployerSize | Small, Medium, Large |

---

## **DIM_Product**

| Column Name | Description |
|-------------|-------------|
| ProductID | Unique product ID |
| ProductName | Product category |
| BenefitType | Health, Dental, Retirement, Life, etc. |

---

## **DIM_Client**

| Column Name | Description |
|-------------|-------------|
| ClientID | Unique client ID |
| AgeGroup | Age segmentation |
| Gender | Gender |
| Province | Client province |

---

## **DIM_Advisor**

| Column Name | Description |
|-------------|-------------|
| AdvisorID | Unique advisor ID |
| AdvisorName | Advisor name |
| Region | Assigned region |

---

## **DIM_Provider**

| Column Name | Description |
|-------------|-------------|
| ProviderID | Healthcare provider ID |
| ProviderType | Hospital, Clinic, Specialist |
| Province | Provider province |

---

# 📈 **Key Measures (DAX)**

---

## **Financial Metrics**

| Measure | Description |
|----------|-------------|
| Premiums Collected | Total premium inflow |
| Claims Paid | Total claims paid |
| Net Margin | Premiums - Claims |
| Loss Ratio | Claims Paid / Premiums Collected |
| Premium Growth % | MoM premium growth |
| Premiums MoM Change | Month-over-month premium variance |
| Claims MoM Change | Month-over-month claims variance |

---

## **Risk Metrics**

| Measure | Description |
|----------|-------------|
| High Severity Claim % | % of claims above severity threshold |
| Loss Ratio (Executive) | Executive formatted loss ratio |

---

## **Revenue Concentration Metrics**

| Measure | Description |
|----------|-------------|
| Employer Revenue Rank | Rank by premium contribution |
| Cumulative Premiums | Running total of premiums |
| Cumulative Premium % | Running % of total portfolio |
| 80% Concentration Threshold | Pareto threshold benchmark |

---

## **Service & Operations Metrics**

| Measure | Description |
|----------|-------------|
| Avg Resolution Days | Average issue resolution time |
| SLA Met % | % of requests meeting SLA |
| SLA Breach % | % exceeding SLA |
| Avg CSAT | Average customer satisfaction score |

---

## **Data Quality Metrics**

| Measure | Description |
|----------|-------------|
| Avg DQ Score | Average data quality score |
| Issue Rate % | Data issue rate |
| Records Checked | Total records validated |

---

## **Targets & Benchmarks**

| Measure | Description |
|----------|-------------|
| Loss Ratio Target | 75% target benchmark |
| SLA Target % | SLA benchmark |
| CSAT Target | Customer satisfaction target |
| Net Margin Target | Margin benchmark |
| 80% Concentration Threshold | Revenue concentration benchmark |

---

# 🧠 **Business Definitions**

**Loss Ratio**  
Claims Paid ÷ Premiums Collected  
Indicates profitability pressure.

**Net Margin**  
Premiums Collected − Claims Paid  
Represents retained earnings before expenses.

**High Severity Claim**  
Claims above predefined percentile threshold.

**Revenue Concentration**  
Cumulative premium contribution by top employers.

**SLA Met %**  
Percentage of service requests resolved within target timeframe.

---

# 📌 **Notes**

- Data is synthetic and generated using Python.
- Designed to simulate enterprise insurance / benefits portfolio analytics.
- Model built using Power BI Star Schema best practices.
- Measures organized into governance folders for maintainability.

---

**Author:** Vinay Verma  
**Project Type:** Insurance / Enterprise Benefits Analytics  
**Tools:** Power BI | DAX | Python  

