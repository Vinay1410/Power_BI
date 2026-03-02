"""
Insurance & Benefits KPI Demo Dataset Generator
- Creates a generic, fictional dataset for BI / governance / KPI dashboards.
- Outputs: CSVs + a ZIP archive.
- Includes BOTH:
  1) DimClient_original_with_messy_province.csv (raw-like messy feed)
  2) DimClient.csv (standardized province codes for reporting)

Dependencies:
  py -m pip install pandas numpy faker
"""

from __future__ import annotations

import os
import re
import zipfile
import string
import random
import datetime as dt
from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker


# -----------------------------
# CONFIG
# -----------------------------
SEED = 42

# Output folder name (created automatically)
OUT_DIR_NAME = "insurer_kpi_dataset"

# Row volumes (adjust if needed)
N_CLIENTS = 12000
N_ADVISORS = 600
N_EMPLOYERS = 650
N_PROVIDERS = 1600
N_POLICIES = 28000
N_TXN = 420000
N_CLAIMS = 140000
N_REQUESTS = 85000


# -----------------------------
# HELPERS
# -----------------------------
PROVINCES = [
    ("ON","Ontario"),("QC","Quebec"),("BC","British Columbia"),("AB","Alberta"),
    ("MB","Manitoba"),("SK","Saskatchewan"),("NS","Nova Scotia"),("NB","New Brunswick"),
    ("NL","Newfoundland and Labrador"),("PE","Prince Edward Island"),
    ("NT","Northwest Territories"),("YT","Yukon"),("NU","Nunavut")
]
PROV_CODES = [p[0] for p in PROVINCES]
PROV_NAME = dict(PROVINCES)

# realistic Canadian distribution (rough estimate)
PROV_W = np.array([0.42,0.23,0.13,0.09,0.05,0.03,0.02,0.015,0.01,0.005,0.002,0.002,0.001])
PROV_W = PROV_W / PROV_W.sum()

digits = np.array(list(string.digits))


def gen_ids(rng: np.random.Generator, prefix: str, n: int, k: int) -> list[str]:
    """Generate stable-looking IDs like CLT#########."""
    n = int(n); k = int(k)
    arr = rng.choice(digits, size=(n, k))
    return [prefix + "".join(row) for row in arr]


def noisy_province(code: str) -> str | None:
    """Intentional messy values to mimic source-system issues."""
    r = random.random()
    if r < 0.80: return code
    if r < 0.86: return code + " "                      # trailing space
    if r < 0.90: return PROV_NAME[code]                 # full name
    if r < 0.93 and code == "QC": return "Q.C."         # punctuation variant
    if r < 0.96 and code == "ON": return "Ont"          # alt abbreviation
    if r < 0.98: return code.lower()                    # case issue
    return None                                         # missing


PROV_MAP = {
    "ON":"ON","ONT":"ON","ONTARIO":"ON",
    "QC":"QC","QUEBEC":"QC","Q C":"QC","QC ":"QC","Q.C":"QC","Q.C.":"QC",
    "BC":"BC","BRITISH COLUMBIA":"BC",
    "AB":"AB","ALBERTA":"AB",
    "MB":"MB","MANITOBA":"MB",
    "SK":"SK","SASKATCHEWAN":"SK",
    "NB":"NB","NEW BRUNSWICK":"NB",
    "NS":"NS","NOVA SCOTIA":"NS",
    "NL":"NL","NEWFOUNDLAND AND LABRADOR":"NL",
    "PE":"PE","PRINCE EDWARD ISLAND":"PE",
    "NT":"NT","NORTHWEST TERRITORIES":"NT",
    "YT":"YT","YUKON":"YT",
    "NU":"NU","NUNAVUT":"NU",
}


def normalize_prov(x) -> str:
    """Standardize provinces into 2-letter codes; fallback Unknown."""
    if pd.isna(x):
        return "Unknown"
    s = str(x).strip()
    if not s:
        return "Unknown"
    s_up = s.upper().replace(".", "")
    s_up = re.sub(r"\s+", " ", s_up).strip()
    if s_up in PROV_MAP:
        return PROV_MAP[s_up]
    s2 = s_up.replace(" ", "")
    if s2 in PROV_MAP:
        return PROV_MAP[s2]
    return "Unknown"


def safe_makedirs(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def zip_folder(folder: Path, zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in folder.glob("*"):
            if p.is_file():
                z.write(p, arcname=p.name)


# -----------------------------
# MAIN
# -----------------------------
def main():
    # deterministic seeds (note: Faker strings can still vary by version; KPIs/logic remains consistent)
    rng = np.random.default_rng(SEED)
    random.seed(SEED)

    fake = Faker("en_CA")
    Faker.seed(SEED)

    # Output folder is next to this script (robust)
    script_dir = Path(__file__).resolve().parent
    out_dir = script_dir / OUT_DIR_NAME
    safe_makedirs(out_dir)

    # -----------------------------
    # DimDate
    # -----------------------------
    date_dim = pd.date_range("2023-01-01", "2025-12-31", freq="D")
    dim_date = pd.DataFrame({"Date": date_dim})
    dim_date["DateKey"] = dim_date["Date"].dt.strftime("%Y%m%d").astype(int)
    dim_date["Year"] = dim_date["Date"].dt.year
    dim_date["Quarter"] = dim_date["Date"].dt.quarter
    dim_date["MonthNum"] = dim_date["Date"].dt.month
    dim_date["Month"] = dim_date["Date"].dt.strftime("%b")
    dim_date["MonthYear"] = dim_date["Date"].dt.strftime("%Y-%m")
    dim_date.to_csv(out_dir / "DimDate.csv", index=False)

    # -----------------------------
    # DimProduct
    # -----------------------------
    products = [
        ("GB_HEALTH","Group Benefits - Health","Benefits",0.30),
        ("GB_DENTAL","Group Benefits - Dental","Benefits",0.25),
        ("GB_STD","Group Benefits - Short Term Disability","Benefits",0.08),
        ("GB_LTD","Group Benefits - Long Term Disability","Benefits",0.06),
        ("IND_LIFE_TERM","Individual - Term Life","Insurance",0.10),
        ("IND_LIFE_PERM","Individual - Permanent Life","Insurance",0.06),
        ("IND_HEALTH","Individual - Health","Insurance",0.03),
        ("GRS_DC","Group Retirement - DC","Retirement",0.07),
        ("GRS_RRSP","Group Retirement - Group RRSP","Retirement",0.03),
        ("WEALTH_SEG","Wealth - Segregated Funds","Wealth",0.02),
    ]
    dim_product = pd.DataFrame(products, columns=["ProductCode","ProductName","LineOfBusiness","MixWeight"])
    dim_product.to_csv(out_dir / "DimProduct.csv", index=False)
    prod_codes = dim_product["ProductCode"].to_numpy()
    prod_weights = (dim_product["MixWeight"] / dim_product["MixWeight"].sum()).to_numpy()

    # -----------------------------
    # DimEmployer
    # -----------------------------
    industry = ["Manufacturing","Tech","Public Sector","Retail","Financial Services","Healthcare","Construction",
                "Education","Transportation","Hospitality"]
    size_bucket = ["<50","50-199","200-999","1000+"]

    dim_employer = pd.DataFrame({
        "EmployerID": gen_ids(rng, "EMP", N_EMPLOYERS, 8),
        "EmployerName": [fake.company() for _ in range(N_EMPLOYERS)],
        "Industry": rng.choice(industry, size=N_EMPLOYERS),
        "SizeBucket": rng.choice(size_bucket, size=N_EMPLOYERS, p=[0.35,0.30,0.25,0.10]),
        "Province": rng.choice(PROV_CODES, size=N_EMPLOYERS, p=PROV_W),
        "City": [fake.city() for _ in range(N_EMPLOYERS)],
    })
    dim_employer.to_csv(out_dir / "DimEmployer.csv", index=False)

    # -----------------------------
    # DimAdvisor
    # -----------------------------
    channels = ["Career Sales Force","Independent Advisor","Bank/Partner","Digital/Direct","Group Plan Sponsor"]
    adv_prov = rng.choice(PROV_CODES, size=N_ADVISORS, p=PROV_W)

    dim_advisor = pd.DataFrame({
        "AdvisorID": gen_ids(rng, "ADV", N_ADVISORS, 7),
        "AdvisorName": [fake.name() for _ in range(N_ADVISORS)],
        "Channel": rng.choice(channels, size=N_ADVISORS, p=[0.35,0.40,0.10,0.10,0.05]),
        "Province": adv_prov,
        "ActiveFlag": (rng.random(N_ADVISORS) > 0.07).astype(int),
        "Email": [fake.email() for _ in range(N_ADVISORS)],
    })
    dim_advisor.to_csv(out_dir / "DimAdvisor.csv", index=False)

    # -----------------------------
    # DimProvider
    # -----------------------------
    provider_types = ["Dental Clinic","Pharmacy","Physio/Chiro","Vision Provider","Specialist Clinic"]
    dim_provider = pd.DataFrame({
        "ProviderID": gen_ids(rng, "PRV", N_PROVIDERS, 8),
        "ProviderName": [fake.company() for _ in range(N_PROVIDERS)],
        "ProviderType": rng.choice(provider_types, size=N_PROVIDERS, p=[0.22,0.30,0.20,0.12,0.16]),
        "Province": rng.choice(PROV_CODES, size=N_PROVIDERS, p=PROV_W),
        "City": [fake.city() for _ in range(N_PROVIDERS)],
    })
    dim_provider.to_csv(out_dir / "DimProvider.csv", index=False)

    # -----------------------------
    # DimClient (RAW + GOLD)
    # -----------------------------
    client_ids = np.array(gen_ids(rng, "CLT", N_CLIENTS, 9), dtype=object)
    natural = np.array(gen_ids(rng, "C", N_CLIENTS, 10), dtype=object)

    # small duplicates in natural key
    dup_count = max(20, int(N_CLIENTS * 0.003))
    dup_ix = rng.choice(np.arange(N_CLIENTS), size=dup_count, replace=False)
    natural[dup_ix] = natural[rng.choice(np.arange(N_CLIENTS), size=dup_count, replace=True)]

    prov_clean = rng.choice(PROV_CODES, size=N_CLIENTS, p=PROV_W)
    province_raw = [noisy_province(c) for c in prov_clean]
    province_std = [normalize_prov(x) for x in province_raw]

    employer_ids = np.where(rng.random(N_CLIENTS) < 0.55, rng.choice(dim_employer["EmployerID"], size=N_CLIENTS), None).astype(object)
    advisor_ids = np.where(rng.random(N_CLIENTS) < 0.70, rng.choice(dim_advisor["AdvisorID"], size=N_CLIENTS), None).astype(object)

    dim_client_raw = pd.DataFrame({
        "ClientID": client_ids,
        "ClientNaturalKey": natural,
        "FirstName": [fake.first_name() for _ in range(N_CLIENTS)],
        "LastName": [fake.last_name() for _ in range(N_CLIENTS)],
        "Age": rng.integers(18, 81, size=N_CLIENTS),
        "Province": province_raw,  # messy
        "City": [fake.city() for _ in range(N_CLIENTS)],
        "EmployerID": employer_ids,
        "AdvisorID": advisor_ids,
    })
    dim_client_raw.to_csv(out_dir / "DimClient_original_with_messy_province.csv", index=False)

    dim_client_gold = dim_client_raw.copy()
    dim_client_gold["Province"] = province_std  # standardized
    dim_client_gold.to_csv(out_dir / "DimClient.csv", index=False)

    # -----------------------------
    # FactPolicy (fast vectorized)
    # -----------------------------
    policy_ids = np.array(gen_ids(rng, "POL", N_POLICIES, 10), dtype=object)
    client_pick = rng.integers(0, N_CLIENTS, size=N_POLICIES)

    client_ref = client_ids[client_pick]
    emp_ref = employer_ids[client_pick]
    adv_ref = advisor_ids[client_pick]
    prod_ref = rng.choice(prod_codes, size=N_POLICIES, p=prod_weights).astype(object)

    start_dates = pd.to_datetime(rng.choice(pd.date_range("2015-01-01","2025-12-01",freq="D"), size=N_POLICIES))
    end_dates = np.full(N_POLICIES, np.datetime64("NaT"), dtype="datetime64[ns]")
    status = np.array(["Active"] * N_POLICIES, dtype=object)

    older = start_dates < pd.Timestamp("2024-01-01")
    end_mask = older & (rng.random(N_POLICIES) < 0.18)
    status[end_mask] = rng.choice(["Lapsed","Cancelled","Matured"], size=end_mask.sum(), p=[0.55,0.35,0.10])
    end_dates[end_mask] = pd.to_datetime(
        rng.choice(pd.date_range("2018-01-01","2025-12-31",freq="D"), size=end_mask.sum())
    ).to_numpy()

    pay_mode = rng.choice(["Monthly","Bi-Weekly","Annual"], size=N_POLICIES, p=[0.72,0.18,0.10])

    # premium proxy
    premium = np.full(N_POLICIES, np.nan)

    benefit_mask = np.char.startswith(prod_ref.astype(str), "GB_")
    tier = rng.choice(["Single","Couple","Family"], size=N_POLICIES, p=[0.55,0.15,0.30])
    tier_mult = np.vectorize({"Single":1.0,"Couple":1.6,"Family":2.2}.get)(tier[benefit_mask])
    premium[benefit_mask] = np.round(np.clip(rng.normal(85,25, size=benefit_mask.sum()) * tier_mult, 25, 320), 2)

    ret_mask = np.isin(prod_ref, ["GRS_DC","GRS_RRSP","WEALTH_SEG"])
    premium[ret_mask] = np.round(np.clip(rng.normal(0.55,0.20, size=ret_mask.sum()), 0.10, 1.50), 2)

    ins_mask = np.isin(prod_ref, ["IND_LIFE_TERM","IND_LIFE_PERM","IND_HEALTH"])
    # simple insurance premium generation
    prem_ins = rng.normal(95, 35, size=ins_mask.sum())
    premium[ins_mask] = np.round(np.clip(prem_ins, 12, 420), 2)

    fact_policy = pd.DataFrame({
        "PolicyID": policy_ids,
        "ClientID": client_ref,
        "EmployerID": emp_ref,
        "AdvisorID": adv_ref,
        "ProductCode": prod_ref,
        "PolicyStartDate": start_dates.date,
        "PolicyEndDate": pd.to_datetime(end_dates).date,
        "PolicyStatus": status,
        "PaymentMode": pay_mode,
        "PlanTier": np.where(benefit_mask, tier, None),
        "PremiumOrRate": premium,
    })
    fact_policy.to_csv(out_dir / "FactPolicy.csv", index=False)

    # -----------------------------
    # FactTransactions
    # -----------------------------
    months = pd.date_range("2023-01-01","2025-12-01",freq="MS")
    pol_ix = rng.integers(0, N_POLICIES, size=N_TXN)

    pol_ref = policy_ids[pol_ix]
    cl_ref = client_ref[pol_ix]
    adv_ref2 = adv_ref[pol_ix].astype(object)
    emp_ref2 = emp_ref[pol_ix].astype(object)
    prod_ref2 = prod_ref[pol_ix].astype(object)

    base_date = months[rng.integers(0, len(months), size=N_TXN)]
    txn_dates = base_date + pd.to_timedelta(rng.integers(0,28,size=N_TXN), unit="D")
    datekeys = txn_dates.strftime("%Y%m%d").astype(int)

    txn_types = np.array(["Premium Payment"] * N_TXN, dtype=object)
    amt = np.zeros(N_TXN)

    is_ret = np.isin(prod_ref2, ["GRS_DC","GRS_RRSP","WEALTH_SEG"])
    ret_types = rng.choice(["Contribution","Withdrawal","Top-up"], size=is_ret.sum(), p=[0.72,0.18,0.10])
    txn_types[is_ret] = ret_types

    ret_amt = rng.lognormal(7.2,0.7, size=is_ret.sum())
    ret_amt = np.round(np.clip(ret_amt, 25, 9000),2)
    ret_amt[ret_types == "Withdrawal"] *= -1
    amt[is_ret] = ret_amt

    is_prem = ~is_ret
    base_prem = fact_policy.loc[pol_ix[is_prem], "PremiumOrRate"].to_numpy()
    amt[is_prem] = np.round(np.clip(rng.normal(base_prem, np.maximum(1, base_prem*0.08)), 5, 2000), 2)

    txn_status = rng.choice(["Posted","Returned","Pending","Reversed"], size=N_TXN, p=[0.88,0.04,0.05,0.03])
    txn_channel = rng.choice(["PAD","Credit Card","Payroll","EFT","Cheque","Online"], size=N_TXN, p=[0.40,0.08,0.30,0.10,0.05,0.07])

    # introduce some missing advisor IDs (realistic)
    adv_ref2[rng.random(N_TXN) < 0.04] = None

    fact_txn = pd.DataFrame({
        "TxnID": gen_ids(rng, "TXN", N_TXN, 12),
        "TxnDateKey": datekeys,
        "PolicyID": pol_ref,
        "ClientID": cl_ref,
        "AdvisorID": adv_ref2,
        "EmployerID": emp_ref2,
        "ProductCode": prod_ref2,
        "TxnType": txn_types,
        "TxnChannel": txn_channel,
        "TxnStatus": txn_status,
        "Amount": amt
    })
    fact_txn.to_csv(out_dir / "FactTransactions.csv", index=False)

    # -----------------------------
    # FactClaims
    # -----------------------------
    benefit_pols_ix = np.where(np.char.startswith(prod_ref.astype(str), "GB_"))[0]
    pol_ix_c = rng.choice(benefit_pols_ix, size=N_CLAIMS, replace=True)

    pol_ref_c = policy_ids[pol_ix_c]
    cl_ref_c = client_ref[pol_ix_c]
    emp_ref_c = emp_ref[pol_ix_c]

    c_base = months[rng.integers(0, len(months), size=N_CLAIMS)]
    claim_dates = c_base + pd.to_timedelta(rng.integers(0,28,size=N_CLAIMS), unit="D")
    claim_datekeys = claim_dates.strftime("%Y%m%d").astype(int)

    ctype = rng.choice(["Health","Dental","Vision","STD","LTD"], size=N_CLAIMS, p=[0.46,0.34,0.08,0.07,0.05])
    cstatus = rng.choice(["Approved","Denied","Pending","Under Review","Adjusted"], size=N_CLAIMS, p=[0.82,0.07,0.05,0.04,0.02])

    def amt_for(mask, mean, sigma, lo, hi):
        v = rng.lognormal(mean, sigma, size=mask.sum())
        return np.round(np.clip(v, lo, hi), 2)

    claim_amt = np.zeros(N_CLAIMS)
    claim_amt[ctype=="Dental"] = amt_for(ctype=="Dental", 5.7, 0.55, 20, 2500)
    claim_amt[ctype=="Health"] = amt_for(ctype=="Health", 5.5, 0.75, 10, 5000)
    claim_amt[ctype=="Vision"] = amt_for(ctype=="Vision", 5.2, 0.45, 30, 1200)
    claim_amt[ctype=="STD"]    = amt_for(ctype=="STD",    7.9, 0.60, 200, 25000)
    claim_amt[ctype=="LTD"]    = amt_for(ctype=="LTD",    8.3, 0.70, 500, 85000)

    base_days = np.select([ctype=="Dental", ctype=="Health", ctype=="Vision", ctype=="STD", ctype=="LTD"],
                          [4,6,5,12,18], default=6)
    infl = np.where(np.isin(cstatus, ["Pending","Under Review"]), 1.8,
                    np.where(cstatus=="Denied", 1.4, 1.0))
    proc_days = np.clip(rng.normal(base_days*infl, 2.8), 1, 60).astype(int)

    processed_dates = claim_dates + pd.to_timedelta(proc_days, unit="D")
    processed_datekeys = processed_dates.strftime("%Y%m%d").astype(int)

    paid = np.zeros(N_CLAIMS)
    approved = (cstatus == "Approved")
    adjusted = (cstatus == "Adjusted")
    paid[approved] = np.round(claim_amt[approved] * np.clip(rng.normal(0.78,0.12, size=approved.sum()), 0.10, 1.00), 2)
    paid[adjusted] = np.round(claim_amt[adjusted] * np.clip(rng.normal(0.55,0.18, size=adjusted.sum()), 0.05, 0.95), 2)

    denial_reasons = np.array(["Coverage limit","Missing documentation","Not eligible",
                               "Waiting period","Coordination of benefits","Provider issue"])
    den_reason = np.where(cstatus=="Denied", rng.choice(denial_reasons, size=N_CLAIMS), None)

    provider_ids = rng.choice(dim_provider["ProviderID"], size=N_CLAIMS).astype(object)
    provider_ids[rng.random(N_CLAIMS) < 0.03] = None

    severity = rng.choice(["Low","Medium","High"], size=N_CLAIMS, p=[0.75,0.20,0.05])
    dis_mask = np.isin(ctype, ["STD","LTD"])
    severity[dis_mask] = rng.choice(["Low","Medium","High"], size=dis_mask.sum(), p=[0.35,0.45,0.20])

    fact_claims = pd.DataFrame({
        "ClaimID": gen_ids(rng, "CLM", N_CLAIMS, 11),
        "ClaimDateKey": claim_datekeys,
        "ProcessedDateKey": processed_datekeys,
        "PolicyID": pol_ref_c,
        "ClientID": cl_ref_c,
        "EmployerID": emp_ref_c,
        "ClaimType": ctype,
        "ServiceMode": rng.choice(["Online/App","Paper","Provider Direct","Call Centre"], size=N_CLAIMS, p=[0.55,0.10,0.25,0.10]),
        "ProviderID": provider_ids,
        "ClaimAmount": claim_amt,
        "PaidAmount": paid,
        "ClaimStatus": cstatus,
        "DenialReason": den_reason,
        "Severity": severity,
    })
    fact_claims.to_csv(out_dir / "FactClaims.csv", index=False)

    # -----------------------------
    # FactServiceRequests
    # -----------------------------
    req_dates = months[rng.integers(0,len(months),size=N_REQUESTS)] + pd.to_timedelta(rng.integers(0,28,size=N_REQUESTS), unit="D")
    req_datekeys = req_dates.strftime("%Y%m%d").astype(int)

    req_types = rng.choice(
        ["Claim Inquiry","Coverage Question","Address Change","Beneficiary Update","Payment Issue",
         "Plan Setup","Password Reset","Appeal","Advisor Support"],
        size=N_REQUESTS,
        p=[0.22,0.16,0.10,0.06,0.14,0.05,0.12,0.07,0.08]
    )
    touch = rng.choice(["Call Centre","Chat","Email","Advisor Portal","Client Portal/App"], size=N_REQUESTS, p=[0.36,0.10,0.14,0.18,0.22])
    res = rng.choice(["Resolved","Escalated","Pending"], size=N_REQUESTS, p=[0.78,0.14,0.08])

    sla_map = {"Claim Inquiry":2,"Coverage Question":2,"Address Change":3,"Beneficiary Update":5,"Payment Issue":2,
               "Plan Setup":7,"Password Reset":1,"Appeal":10,"Advisor Support":2}
    sla = np.array([sla_map[t] for t in req_types])
    sev = rng.choice(["Low","Medium","High"], size=N_REQUESTS, p=[0.70,0.25,0.05])

    base = sla * (1.0 + np.where(sev=="Medium",0.2,np.where(sev=="High",0.6,0.0)))
    act = np.clip(rng.normal(base, 1.3), 0, 30).astype(int)

    closed = np.where(res=="Resolved", (req_dates + pd.to_timedelta(act, unit="D")).strftime("%Y%m%d").astype(int), None)
    csat = np.where((res=="Resolved") & (rng.random(N_REQUESTS)<0.60),
                    np.clip(np.rint(rng.normal(4.2,0.7,size=N_REQUESTS)),1,5).astype(int),
                    None)

    clt_ix = rng.integers(0, N_CLIENTS, size=N_REQUESTS)

    fact_req = pd.DataFrame({
        "RequestID": gen_ids(rng, "REQ", N_REQUESTS, 12),
        "RequestDateKey": req_datekeys,
        "ClosedDateKey": closed,
        "ClientID": client_ids[clt_ix],
        "AdvisorID": advisor_ids[clt_ix],
        "EmployerID": employer_ids[clt_ix],
        "RequestType": req_types,
        "Touchpoint": touch,
        "Severity": sev,
        "SLA_Days": sla,
        "ActualDays": np.where(res=="Resolved", act, None),
        "ResolutionStatus": res,
        "CSAT": csat,
    })
    fact_req.to_csv(out_dir / "FactServiceRequests.csv", index=False)

    # -----------------------------
    # FactDataQualityMonthly
    # -----------------------------
    dq_domains = ["Client Master","Policy Admin","Claims","Advisor","Employer","Transactions"]
    dq_dimensions = ["Completeness","Uniqueness","Validity","Timeliness","Consistency"]

    dq_rows = []
    for m in months:
        for dom in dq_domains:
            for dim in dq_dimensions:
                base_score = {"Client Master":92,"Policy Admin":90,"Claims":88,"Advisor":95,"Employer":91,"Transactions":87}[dom]
                drift = float(rng.normal(0, 1.8))
                incident = float(rng.uniform(-8,-3)) if random.random() < 0.05 else 0.0
                score = float(np.clip(base_score + drift + incident, 70, 99.5))
                dq_rows.append({
                    "MonthYear": m.strftime("%Y-%m"),
                    "Domain": dom,
                    "DQDimension": dim,
                    "DQScore": round(score, 2),
                    "RecordsChecked": int(rng.integers(80_000, 1_600_000)),
                    "IssueCount": int(max(0, rng.normal((100-score)*35, 120))),
                })

    fact_dq = pd.DataFrame(dq_rows)
    fact_dq.to_csv(out_dir / "FactDataQualityMonthly.csv", index=False)

    # -----------------------------
    # README
    # -----------------------------
    readme = """Insurance & Benefits KPI Demo Dataset (Simulated)

Purpose:
- Generic, fictional dataset to demonstrate KPI dashboards + data governance for an insurer / benefits administrator.

Tables:
Dimensions: DimDate, DimClient, DimAdvisor, DimEmployer, DimProduct, DimProvider
Facts: FactPolicy, FactTransactions, FactClaims, FactServiceRequests, FactDataQualityMonthly

Notes:
- DimClient_original_with_messy_province.csv mimics source-system inconsistencies.
- DimClient.csv contains standardized provinces for reporting ("gold" layer).
- Missing ProviderID/AdvisorID appear in a small % of rows to demonstrate referential integrity handling.
"""
    (out_dir / "README.txt").write_text(readme, encoding="utf-8")

    # -----------------------------
    # ZIP OUTPUT
    # -----------------------------
    zip_path = script_dir / f"{OUT_DIR_NAME}.zip"
    zip_folder(out_dir, zip_path)

    print("\n✅ Dataset generated successfully!")
    print("Output folder:", out_dir)
    print("ZIP file:", zip_path)


if __name__ == "__main__":
    main()
