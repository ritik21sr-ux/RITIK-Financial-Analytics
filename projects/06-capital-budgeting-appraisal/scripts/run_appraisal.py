#!/usr/bin/env python3
"""Calculate synthetic five-year project cash flows, NPV, IRR, and sensitivity."""

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCENARIO_FILE = ROOT / "data" / "scenario_assumptions.csv"


def read_scenarios():
    with SCENARIO_FILE.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    numeric = [name for name in rows[0] if name != "scenario"]
    for row in rows:
        for field in numeric:
            row[field] = float(row[field])
    return {row["scenario"]: row for row in rows}


def cash_flows(a, revenue_multiplier=1.0):
    revenues = [a["year1_revenue_inr"] * revenue_multiplier * (1 + a["revenue_growth_pct"]) ** i for i in range(5)]
    nwc = [revenue * a["working_capital_pct"] for revenue in revenues]
    depreciation = a["initial_capex_inr"] / 5
    flows = [{
        "year": 0, "revenue_inr": 0, "gross_profit_inr": 0, "operating_expense_inr": 0,
        "depreciation_inr": 0, "ebit_inr": 0, "cash_taxes_inr": 0,
        "capex_inr": a["initial_capex_inr"], "change_nwc_inr": nwc[0],
        "free_cash_flow_inr": -a["initial_capex_inr"] - nwc[0],
    }]
    for year in range(1, 6):
        revenue = revenues[year - 1]
        gross_profit = revenue * a["gross_margin_pct"]
        operating_expense = a["year1_opex_inr"] * (1 + a["opex_growth_pct"]) ** (year - 1)
        ebit = gross_profit - operating_expense - depreciation
        taxes = max(ebit, 0) * a["tax_rate_pct"]
        if year < 5:
            change_nwc = nwc[year] - nwc[year - 1]
        else:
            change_nwc = -nwc[year - 1]
        maintenance = a["annual_maintenance_capex_inr"]
        fcf = ebit - taxes + depreciation - maintenance - change_nwc
        flows.append({
            "year": year, "revenue_inr": round(revenue, 2), "gross_profit_inr": round(gross_profit, 2),
            "operating_expense_inr": round(operating_expense, 2), "depreciation_inr": round(depreciation, 2),
            "ebit_inr": round(ebit, 2), "cash_taxes_inr": round(taxes, 2),
            "capex_inr": round(maintenance, 2), "change_nwc_inr": round(change_nwc, 2),
            "free_cash_flow_inr": round(fcf, 2),
        })
    return flows


def npv(flows, rate):
    return sum(row["free_cash_flow_inr"] / ((1 + rate) ** row["year"]) for row in flows)


def irr(flows):
    def value(rate):
        return npv(flows, rate)
    low, high = -0.90, 1.0
    while value(high) > 0 and high < 100:
        high = high * 2 + 1
    if value(low) * value(high) > 0:
        return None
    for _ in range(160):
        mid = (low + high) / 2
        if value(mid) > 0:
            low = mid
        else:
            high = mid
    return (low + high) / 2


def discounted_payback(flows, rate):
    cumulative = 0.0
    previous = 0.0
    for row in flows:
        previous = cumulative
        pv = row["free_cash_flow_inr"] / ((1 + rate) ** row["year"])
        cumulative += pv
        if cumulative >= 0 and row["year"] > 0:
            inflow = cumulative - previous
            fraction = -previous / inflow if inflow else 0
            return round(row["year"] - 1 + fraction, 2)
    return "Not reached"


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    scenarios = read_scenarios()
    summaries = []
    all_flows = {}
    for name in ("Base", "Downside", "Upside"):
        a = scenarios[name]
        flows = cash_flows(a)
        all_flows[name] = flows
        rate = a["discount_rate_pct"]
        rate_of_return = irr(flows)
        summaries.append({
            "scenario": name,
            "discount_rate_pct": round(rate, 4),
            "year1_revenue_inr": round(a["year1_revenue_inr"], 2),
            "initial_investment_inr": round(a["initial_capex_inr"] + a["year1_revenue_inr"] * a["working_capital_pct"], 2),
            "five_year_npv_inr": round(npv(flows, rate), 2),
            "irr_pct": round(rate_of_return, 4) if rate_of_return is not None else "",
            "discounted_payback_years": discounted_payback(flows, rate),
        })

    write_csv(ROOT / "examples" / "scenario_summary.csv", summaries)
    base = scenarios["Base"]
    base_flows = cash_flows(base)
    base_rate = base["discount_rate_pct"]
    schedule = []
    cumulative = 0.0
    for row in base_flows:
        factor = 1 / ((1 + base_rate) ** row["year"])
        pv = row["free_cash_flow_inr"] * factor
        cumulative += pv
        schedule.append({**row, "discount_factor": round(factor, 6), "present_value_inr": round(pv, 2), "cumulative_pv_inr": round(cumulative, 2)})
    write_csv(ROOT / "examples" / "base_cash_flows.csv", schedule)

    rates = [0.08, 0.10, 0.12, 0.14, 0.16]
    multipliers = [0.80, 0.90, 1.00, 1.10, 1.20]
    sensitivity = []
    for multiplier in multipliers:
        flows = cash_flows(base, multiplier)
        sensitivity.append({"revenue_multiplier": multiplier, **{f"npv_at_{int(rate*100)}pct_inr": round(npv(flows, rate), 2) for rate in rates}})
    write_csv(ROOT / "examples" / "npv_sensitivity.csv", sensitivity)
    summary = {"dataset": "synthetic portfolio demonstration", "scenarios": summaries, "sensitivity_base": "Base assumptions; revenue level and discount rate varied"}
    (ROOT / "examples" / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
