\# Data Dictionary — Fact\_Lease\_Returns



| Column | Type | Description |

|-------|------|-------------|

| Lease\_ID | Integer | Unique lease identifier |

| Model\_Code | Text | Vehicle model code |

| Segment | Text | Vehicle body type (Compact / Sedan / SUV) |

| Return\_Year | Integer | Lease end year |

| Residual\_Value | Decimal | Forecasted RV at lease-end |

| Actual\_Sale\_Price | Decimal | Realized sale price at disposal |

| Gain\_Loss\_Amount | Decimal | Actual Sale Price - Residual Value |

| Gain\_Loss\_Pct | Decimal | Gain/Loss % relative to Residual Value |

| Mileage\_At\_Return | Integer | Vehicle mileage at lease return |

| Region | Text | Province code (ON, QC, AB, BC, etc.) |

| Latitude | Decimal | Province centroid latitude |

| Longitude | Decimal | Province centroid longitude |

| Mileage Band | Text | Binned mileage band for visualization |



