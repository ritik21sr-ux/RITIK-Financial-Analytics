#!/usr/bin/env python3
"""Generate a deterministic synthetic 2025 order-line dataset."""

import csv
import random
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
random.seed(7035)
CUSTOMERS = [
    (f"CU{i:03d}", f"Customer {i:03d}", random.choices(["SMB", "Mid-market", "Enterprise"], [55, 32, 13])[0], random.choice(["North", "South", "West", "East"]))
    for i in range(1, 61)
]
PRODUCTS = {
    "Hardware": (0.30, 22000, 125000),
    "Software": (0.72, 8000, 68000),
    "Services": (0.52, 6000, 56000),
    "Supplies": (0.25, 1500, 18000),
    "Accessories": (0.38, 2500, 24000),
    "Freight": (0.10, 800, 9500),
}


def main():
    rows = []
    invoice_number = 1
    for customer_id, customer_name, segment, region in CUSTOMERS:
        order_count = random.randint(4, 10)
        for _ in range(order_count):
            month = random.randint(1, 12)
            invoice_date = date(2025, month, 1) + timedelta(days=random.randint(0, 27))
            invoice_id = f"INV-{invoice_number:05d}"
            invoice_number += 1
            for _line in range(random.randint(1, 3)):
                product = random.choice(list(PRODUCTS))
                margin, low, high = PRODUCTS[product]
                units = random.randint(1, 12)
                price = random.randrange(low // 100, high // 100 + 1) * 100
                gross = units * price
                discount_rate = random.choice([0, 0.03, 0.05, 0.08, 0.12, 0.16, 0.20])
                discount = round(gross * discount_rate)
                returns = round(gross * random.choice([0, 0, 0, 0.02, 0.04]))
                net_revenue = max(0, gross - discount - returns)
                cogs = round(net_revenue * (1 - margin))
                shipping = units * random.randrange(20, 151, 10)
                commission = round(net_revenue * random.choice([0.02, 0.03, 0.04, 0.05]))
                contribution = net_revenue - cogs - shipping - commission
                rows.append({
                    "month": invoice_date.strftime("%Y-%m"),
                    "invoice_date": invoice_date.isoformat(),
                    "invoice_id": invoice_id,
                    "customer_id": customer_id,
                    "customer_name": customer_name,
                    "segment": segment,
                    "region": region,
                    "product": product,
                    "units": units,
                    "list_price_inr": price,
                    "gross_sales_inr": gross,
                    "discount_inr": discount,
                    "returns_inr": returns,
                    "net_revenue_inr": net_revenue,
                    "cogs_inr": cogs,
                    "shipping_inr": shipping,
                    "sales_commission_inr": commission,
                    "contribution_inr": contribution,
                })

    path = ROOT / "data" / "sales_lines.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} synthetic order lines across {len(CUSTOMERS)} customers")


if __name__ == "__main__":
    main()
