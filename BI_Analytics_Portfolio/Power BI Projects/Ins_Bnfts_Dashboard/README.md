# 📊 **Enterprise Benefits Performance & Risk Dashboard**

An end-to-end Power BI dashboard analyzing financial performance, claims risk, service operations, and portfolio concentration across an enterprise benefits portfolio.

> ⚠️ All data is simulated using Python for demonstration purposes. No confidential data is included.

  ⚠️ **Disclaimer**: All datasets in this repository are synthetically generated using Python to simulate real-world business scenarios; while designed to closely mirror practical conditions, simulated data may occasionally produce anomalies or edge-case behaviors in visuals—these are inherent to the synthetic modeling process and should be viewed as part of the simulation context, with focus placed on the BI architecture, analytical logic, and data modeling capabilities demonstrated.

---

## 🔎 **Project Objective**

This project demonstrates how to design an executive-level performance dashboard that answers key business questions:

- Are we profitable?
- Is risk under control?
- Are claims trending above target?
- Are we overly dependent on a few large employers?
- Is service performance impacting financial outcomes?

The dashboard showcases financial analytics, risk monitoring, operational KPIs, portfolio concentration analysis, and executive storytelling using Power BI and DAX.

---

# 🧱 **Architecture Overview**

## **Data Generation**
- Synthetic enterprise-style insurance data generated using Python  
- Exported to CSV files  
- Loaded into Power BI  
- Modeled using a Star Schema  

## **Data Model (Star Schema)**

### **Dimension Tables**
- `DIM_Date`
- `DIM_Product`
- `DIM_Employer`
- `DIM_Advisor`
- `DIM_Client`
- `DIM_Provider`

### **Fact Tables**
- `FACT_Policy`
- `FACT_Claims`
- `FACT_Transactions`
- `FACT_ServiceRequests`
- `FACT_DataQualityMonthly`

---

# 🐍 **Python Data Simulation**

Raw enterprise-style insurance data was generated using Python to simulate:

- Monthly premium inflows  
- Claims frequency & severity  
- Loss ratios  
- Service SLA performance  
- High severity claim distribution  
- Employer-level portfolio concentration  
- Data quality scoring  

### **Example Business Logic Simulated**

- Claims follow a probabilistic distribution
- High severity claims assigned based on percentile thresholds
- Loss ratio calculated as:
```
Loss_Ratio = Claims_Paid / Premiums_Collected
```

- Service resolution days randomly distributed with SLA targets
- Revenue concentration modeled using skewed employer revenue patterns

This allows realistic testing of:
- Month-over-month variance
- Target breaches
- Risk concentration
- Portfolio diversification exposure

---

# 📈 **Dashboard Pages**

---

## 1️⃣ **Executive Overview**

### **Portfolio Snapshot KPIs**
- Premiums Collected  
- Claims Paid  
- Net Margin  
- Average Data Quality Score  

### **Risk & Profitability**
- Loss Ratio vs Target  
- High Severity Claim %  
- Dynamic variance vs goal  

### **Service & Experience**
- Avg CSAT  
- SLA Met %  
- Avg Claim Processing
- Avg Resolution Days  

### **Executive Headline**
Dynamic DAX narrative that changes based on:
- Loss ratio vs target
- Margin performance
- Risk movement

---

## 2️⃣ **Financial Performance**

### 🔹 **Net Margin Bridge (Waterfall)**

Premiums → Claims → Net Margin

Example DAX:

```DAX
Bridge Amount =
SWITCH(
    SELECTEDVALUE('Financial Bridge'[BridgeItem]),
    "Premiums Collected", [Premiums Collected],
    "Claims Paid", -[Claims Paid],
    "Net Margin", [Net Margin]
)
```

Demonstrates:
- Margin retained %
- Claims pressure impact
- Profitability decomposition

---

### 🔹 **Revenue Concentration (Pareto Analysis)**

Top 20 Employers cumulative revenue percentage.

Key Measures:

```DAX
Employer Revenue Rank =
RANKX(
    ALL(DIM_Employer[EmployerName]),
    [Premiums Collected],
    ,
    DESC,
    DENSE
)

Cumulative Premium % =
DIVIDE(
    [Cumulative Premiums],
    [Total Premiums (All Employers)]
)
```

Insight:
Top 20 employers contribute ~49% of total premiums, indicating portfolio diversification strength.

---

### 🔹 **Premiums & Loss Ratio Trend**

Combo chart analyzing:
- Monthly premiums
- Monthly loss ratio
- 75% loss ratio target

Enables:
- Target breach detection
- Margin pressure analysis
- Risk spike identification

---

### 🔹 **Risk vs Scale (Scatter Plot)**

Employer-level analysis:

- X-axis: Revenue (Premiums)
- Y-axis: Claims Cost Ratio
- Reference line: 75% target

Used to identify:
- Large but risky accounts
- High-loss small employers
- Risk-adjusted profitability positioning

---

# 📐 **DAX Highlights**

Key analytical logic implemented:

- `RANKX` for employer revenue ranking
- `CALCULATE` with context transitions
- `SWITCH` for dynamic measure logic
- Target benchmarking framework
- Dynamic narrative text measures
- Concentration curve calculation
- Waterfall modeling using custom bridge table

---

# 🧠 **Analytical Themes Demonstrated**

- Loss ratio monitoring
- Portfolio concentration risk
- Month-over-month premium growth
- Claims severity tracking
- SLA performance monitoring
- Risk-adjusted employer profitability
- Executive KPI storytelling
- Target benchmarking system
- Clean measure governance

---

# 🗂 **Measure Governance Structure**

Measures organized into logical folders:

- Executive KPIs
- Financial KPIs
- Claims
- Operations
- Revenue Concentration
- Employer Analytics
- Targets
- Bridge (Waterfall)
- Data Quality
- Utility

This improves maintainability and scalability of the model.

---

# 🛠 **Tools Used**

- Power BI Desktop  
- DAX  
- Python (pandas, numpy)  
- GitHub  

---

# 🚀 **Why This Project Matters**

This dashboard simulates real-world enterprise insurance portfolio monitoring and demonstrates:

- Business-first analytical thinking
- Risk management awareness
- Financial KPI modeling
- Executive storytelling capability
- Advanced DAX proficiency
- Clean data modeling practices


---

## 📌 **Disclaimer**

All data used in this project is synthetically generated using Python for portfolio demonstration purposes only. No real client, employer, or policy data is included.

---

**Author:** Vinay Verma  
**Location:** Canada  
**Tools:** Power BI | DAX | Python | Power Query  