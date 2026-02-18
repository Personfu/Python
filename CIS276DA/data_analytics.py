# ============================================================
# Data Analytics Pipeline
# CIS 276DA -- Advanced SQL & Data Analytics | FLLC Enterprise
# Author: Preston Furulie
# ============================================================
# Covers: data cleaning & normalization, statistical analysis,
# ASCII visualization, ETL simulation, aggregation & grouping,
# trend analysis, moving averages, and CSV processing.
# ============================================================

import csv
import io
import os
import math
from collections import Counter, defaultdict
from datetime import datetime, timedelta


# ============================================================
# SECTION 0: SAMPLE DATA GENERATION
# Simulates the my_guitar_shop dataset for standalone use.
# ============================================================

CATEGORIES = {1: "Guitars", 2: "Basses", 3: "Drums"}

PRODUCTS_CSV = """\
product_id,category_id,product_name,list_price,discount_percent,date_added
1,1,Fender Stratocaster,1199.00,15,2024-06-15
2,1,Gibson Les Paul,2499.00,10,2024-07-01
3,1,PRS Custom 24,3599.00,5,2024-08-10
4,1,Ibanez RG550,899.00,20,2024-05-20
5,2,Fender Jazz Bass,1149.00,12,2024-06-25
6,2,Music Man StingRay,2199.00,8,2024-09-01
7,3,Pearl Export Kit,799.00,18,2024-04-10
8,3,DW Collector Series,3299.00,0,2024-10-05
9,1,Epiphone SG,449.00,25,2024-03-15
10,3,Roland TD-17,1599.00,10,2024-07-22
"""

ORDERS_CSV = """\
order_id,customer_id,product_id,quantity,item_price,discount_amount,order_date,ship_date
101,1,1,1,1199.00,179.85,2025-01-10,2025-01-13
102,2,2,1,2499.00,249.90,2025-01-15,2025-01-18
103,1,5,1,1149.00,137.88,2025-02-02,2025-02-05
104,3,7,2,799.00,143.82,2025-02-14,2025-02-17
105,2,3,1,3599.00,179.95,2025-03-01,2025-03-05
106,4,9,1,449.00,112.25,2025-03-10,
107,3,10,1,1599.00,159.90,2025-03-22,2025-03-25
108,1,4,1,899.00,179.80,2025-04-05,2025-04-08
109,5,6,1,2199.00,175.92,2025-04-18,
110,2,8,1,3299.00,0.00,2025-05-01,2025-05-04
111,4,1,2,1199.00,179.85,2025-05-15,2025-05-18
112,3,2,1,2499.00,249.90,2025-06-01,2025-06-04
113,1,10,1,1599.00,159.90,2025-06-20,
114,5,7,3,799.00,143.82,2025-07-04,2025-07-07
115,2,4,1,899.00,179.80,2025-07-19,2025-07-22
116,4,3,1,3599.00,179.95,2025-08-02,2025-08-06
117,3,5,2,1149.00,137.88,2025-08-20,2025-08-23
118,1,6,1,2199.00,175.92,2025-09-10,
119,5,9,2,449.00,112.25,2025-09-25,2025-09-28
120,2,8,1,3299.00,0.00,2025-10-12,2025-10-15
"""


def parse_csv(csv_text):
    """Parse a CSV string into a list of dictionaries."""
    reader = csv.DictReader(io.StringIO(csv_text.strip()))
    rows = []
    for row in reader:
        clean = {}
        for k, v in row.items():
            v = v.strip()
            if v == "":
                clean[k] = None
            else:
                try:
                    clean[k] = int(v)
                except ValueError:
                    try:
                        clean[k] = float(v)
                    except ValueError:
                        clean[k] = v
            clean[k] = clean.get(k, v)
        rows.append(clean)
    return rows


# ============================================================
# SECTION 1: ETL -- EXTRACT, TRANSFORM, LOAD
# ============================================================

class ETLPipeline:
    """Simulates a three-stage ETL pipeline."""

    def __init__(self):
        self.raw_products = []
        self.raw_orders = []
        self.clean_products = []
        self.clean_orders = []

    # -- Extract -----------------------------------------------
    def extract(self):
        print("=" * 60)
        print("ETL STAGE 1: EXTRACT")
        print("=" * 60)
        self.raw_products = parse_csv(PRODUCTS_CSV)
        self.raw_orders = parse_csv(ORDERS_CSV)
        print(f"  Extracted {len(self.raw_products)} products")
        print(f"  Extracted {len(self.raw_orders)} orders")
        return self

    # -- Transform ---------------------------------------------
    def transform(self):
        print("\n" + "=" * 60)
        print("ETL STAGE 2: TRANSFORM")
        print("=" * 60)

        null_count = 0
        for p in self.raw_products:
            sale_price = round(
                p["list_price"] * (1 - p["discount_percent"] / 100), 2
            )
            self.clean_products.append({
                "product_id": p["product_id"],
                "category": CATEGORIES.get(p["category_id"], "Unknown"),
                "product_name": p["product_name"],
                "list_price": p["list_price"],
                "discount_percent": p["discount_percent"],
                "sale_price": sale_price,
                "date_added": p["date_added"],
            })

        for o in self.raw_orders:
            if o["ship_date"] is None:
                null_count += 1
            line_total = round(
                (o["item_price"] - o["discount_amount"]) * o["quantity"], 2
            )
            self.clean_orders.append({
                "order_id": o["order_id"],
                "customer_id": o["customer_id"],
                "product_id": o["product_id"],
                "quantity": o["quantity"],
                "item_price": o["item_price"],
                "discount_amount": o["discount_amount"],
                "line_total": line_total,
                "order_date": o["order_date"],
                "ship_date": o["ship_date"],
                "shipped": o["ship_date"] is not None,
            })

        print(f"  Computed sale_price for {len(self.clean_products)} products")
        print(f"  Computed line_total for {len(self.clean_orders)} orders")
        print(f"  Identified {null_count} unshipped orders (NULL ship_date)")
        return self

    # -- Load --------------------------------------------------
    def load(self, output_dir=None):
        print("\n" + "=" * 60)
        print("ETL STAGE 3: LOAD")
        print("=" * 60)
        if output_dir and os.path.isdir(output_dir):
            prod_path = os.path.join(output_dir, "clean_products.csv")
            ord_path = os.path.join(output_dir, "clean_orders.csv")
            self._write_csv(prod_path, self.clean_products)
            self._write_csv(ord_path, self.clean_orders)
            print(f"  Wrote {prod_path}")
            print(f"  Wrote {ord_path}")
        else:
            print("  [Simulation] Would write clean_products.csv")
            print("  [Simulation] Would write clean_orders.csv")
        print(f"  Load complete -- {len(self.clean_products)} products, "
              f"{len(self.clean_orders)} orders")
        return self

    @staticmethod
    def _write_csv(path, rows):
        if not rows:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)


# ============================================================
# SECTION 2: STATISTICAL ANALYSIS
# ============================================================

def mean(values):
    return sum(values) / len(values) if values else 0


def median(values):
    s = sorted(values)
    n = len(s)
    if n == 0:
        return 0
    mid = n // 2
    return (s[mid - 1] + s[mid]) / 2 if n % 2 == 0 else s[mid]


def mode(values):
    counts = Counter(values)
    max_count = max(counts.values())
    modes = [v for v, c in counts.items() if c == max_count]
    return modes


def stdev(values):
    if len(values) < 2:
        return 0
    avg = mean(values)
    variance = sum((x - avg) ** 2 for x in values) / (len(values) - 1)
    return math.sqrt(variance)


def statistical_summary(label, values):
    """Print a statistical summary for a numeric list."""
    print(f"\n{'-' * 50}")
    print(f"Statistical Summary: {label}")
    print(f"{'-' * 50}")
    print(f"  Count:    {len(values)}")
    print(f"  Mean:     ${mean(values):,.2f}")
    print(f"  Median:   ${median(values):,.2f}")
    print(f"  Mode:     {mode(values)}")
    print(f"  Std Dev:  ${stdev(values):,.2f}")
    print(f"  Min:      ${min(values):,.2f}")
    print(f"  Max:      ${max(values):,.2f}")
    print(f"  Range:    ${max(values) - min(values):,.2f}")


# ============================================================
# SECTION 3: ASCII DATA VISUALIZATION
# ============================================================

def horizontal_bar_chart(title, labels, values, bar_char="#", width=40):
    """Render a horizontal bar chart using ASCII characters."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")
    max_val = max(values) if values else 1
    max_label_len = max(len(str(l)) for l in labels) if labels else 10

    for label, val in zip(labels, values):
        bar_len = int((val / max_val) * width) if max_val > 0 else 0
        bar = bar_char * bar_len
        print(f"  {str(label):>{max_label_len}} | {bar} {val:,.2f}")
    print()


def histogram(title, values, bins=5):
    """Render a histogram of numeric values."""
    if not values:
        return
    lo, hi = min(values), max(values)
    bin_width = (hi - lo) / bins if hi != lo else 1
    counts = [0] * bins
    for v in values:
        idx = min(int((v - lo) / bin_width), bins - 1)
        counts[idx] += 1

    labels = []
    for i in range(bins):
        low = lo + i * bin_width
        high = low + bin_width
        labels.append(f"${low:,.0f}-${high:,.0f}")

    horizontal_bar_chart(title, labels, [float(c) for c in counts],
                         bar_char="=", width=30)


def sparkline(values):
    """Return a single-line sparkline string for a series."""
    blocks = " ._-~=+*#@"
    if not values:
        return ""
    lo, hi = min(values), max(values)
    rng = hi - lo if hi != lo else 1
    return "".join(blocks[min(int((v - lo) / rng * 8), 8)] for v in values)


# ============================================================
# SECTION 4: AGGREGATION AND GROUPING
# ============================================================

def group_by(records, key_func):
    """Group a list of dicts by the result of key_func."""
    groups = defaultdict(list)
    for r in records:
        groups[key_func(r)].append(r)
    return dict(groups)


def aggregate_by_category(products):
    """Aggregate product statistics by category."""
    print(f"\n{'=' * 60}")
    print("  Aggregation: Products by Category")
    print(f"{'=' * 60}")
    groups = group_by(products, lambda p: p["category"])
    for cat in sorted(groups):
        items = groups[cat]
        prices = [p["list_price"] for p in items]
        print(f"\n  Category: {cat}")
        print(f"    Count:     {len(items)}")
        print(f"    Avg Price: ${mean(prices):,.2f}")
        print(f"    Min Price: ${min(prices):,.2f}")
        print(f"    Max Price: ${max(prices):,.2f}")
        print(f"    Total:     ${sum(prices):,.2f}")


def aggregate_by_month(orders):
    """Aggregate order revenue by month."""
    print(f"\n{'=' * 60}")
    print("  Aggregation: Monthly Revenue")
    print(f"{'=' * 60}")
    groups = group_by(orders, lambda o: o["order_date"][:7])
    months = sorted(groups.keys())
    labels = []
    values = []
    for m in months:
        month_orders = groups[m]
        revenue = sum(o["line_total"] for o in month_orders)
        labels.append(m)
        values.append(revenue)
        count = len(month_orders)
        print(f"  {m}  |  Orders: {count:>2}  |  Revenue: ${revenue:>10,.2f}")

    print(f"\n  Sparkline: {sparkline(values)}")
    return labels, values


# ============================================================
# SECTION 5: TREND ANALYSIS & MOVING AVERAGES
# ============================================================

def moving_average(values, window=3):
    """Compute a simple moving average with the given window size."""
    if len(values) < window:
        return values[:]
    result = []
    for i in range(len(values)):
        if i < window - 1:
            result.append(None)
        else:
            segment = values[i - window + 1: i + 1]
            result.append(round(sum(segment) / window, 2))
    return result


def trend_analysis(labels, values, window=3):
    """Analyze trends and display a moving average table."""
    print(f"\n{'=' * 60}")
    print(f"  Trend Analysis (SMA window={window})")
    print(f"{'=' * 60}")
    ma = moving_average(values, window)

    print(f"  {'Month':<10} {'Revenue':>12} {'SMA':>12} {'Trend':>10}")
    print(f"  {'-' * 10} {'-' * 12} {'-' * 12} {'-' * 10}")
    for i, (lbl, val) in enumerate(zip(labels, values)):
        ma_str = f"${ma[i]:>10,.2f}" if ma[i] is not None else f"{'---':>11}"
        if i > 0 and ma[i] is not None and ma[i - 1] is not None:
            diff = ma[i] - ma[i - 1]
            trend = "^ Up" if diff > 0 else "v Down" if diff < 0 else "-- Flat"
        else:
            trend = "---"
        print(f"  {lbl:<10} ${val:>10,.2f} {ma_str} {trend:>10}")


def month_over_month_growth(labels, values):
    """Compute and display month-over-month growth rates."""
    print(f"\n{'=' * 60}")
    print("  Month-over-Month Growth")
    print(f"{'=' * 60}")
    for i in range(1, len(values)):
        prev = values[i - 1]
        curr = values[i]
        if prev > 0:
            growth = (curr - prev) / prev * 100
            arrow = "^" if growth > 0 else "v" if growth < 0 else "-"
            print(f"  {labels[i-1]} -> {labels[i]}:  {arrow} {growth:>+7.1f}%")
        else:
            print(f"  {labels[i-1]} -> {labels[i]}:  N/A (zero base)")


# ============================================================
# SECTION 6: DATA CLEANING & NORMALIZATION
# ============================================================

def normalize_min_max(values):
    """Scale values to [0, 1] range using min-max normalization."""
    lo, hi = min(values), max(values)
    rng = hi - lo if hi != lo else 1
    return [round((v - lo) / rng, 4) for v in values]


def normalize_z_score(values):
    """Scale values using z-score normalization (mean=0, stdev=1)."""
    avg = mean(values)
    sd = stdev(values) if stdev(values) != 0 else 1
    return [round((v - avg) / sd, 4) for v in values]


def demonstrate_normalization(products):
    """Show normalization techniques on product prices."""
    print(f"\n{'=' * 60}")
    print("  Data Normalization: Product Prices")
    print(f"{'=' * 60}")
    prices = [p["list_price"] for p in products]
    names = [p["product_name"] for p in products]
    min_max = normalize_min_max(prices)
    z_scores = normalize_z_score(prices)

    print(f"  {'Product':<25} {'Price':>10} {'MinMax':>8} {'Z-Score':>8}")
    print(f"  {'-' * 25} {'-' * 10} {'-' * 8} {'-' * 8}")
    for name, price, mm, z in zip(names, prices, min_max, z_scores):
        print(f"  {name:<25} ${price:>8,.2f} {mm:>8.4f} {z:>+8.4f}")


# ============================================================
# SECTION 7: DECISION SUPPORT QUERIES
# ============================================================

def customer_rfm_analysis(orders):
    """Recency-Frequency-Monetary analysis for customer segmentation."""
    print(f"\n{'=' * 60}")
    print("  Decision Support: Customer RFM Analysis")
    print(f"{'=' * 60}")
    reference_date = datetime(2025, 11, 1)
    customer_data = defaultdict(lambda: {
        "orders": [], "total_spent": 0, "last_order": None
    })

    for o in orders:
        cid = o["customer_id"]
        odate = datetime.strptime(o["order_date"], "%Y-%m-%d")
        customer_data[cid]["orders"].append(o["order_id"])
        customer_data[cid]["total_spent"] += o["line_total"]
        if (customer_data[cid]["last_order"] is None
                or odate > customer_data[cid]["last_order"]):
            customer_data[cid]["last_order"] = odate

    print(f"  {'Cust':>5} {'Recency':>10} {'Freq':>6} {'Monetary':>12} {'Segment':<15}")
    print(f"  {'-' * 5} {'-' * 10} {'-' * 6} {'-' * 12} {'-' * 15}")

    for cid in sorted(customer_data):
        d = customer_data[cid]
        recency = (reference_date - d["last_order"]).days
        frequency = len(set(d["orders"]))
        monetary = d["total_spent"]

        if recency <= 60 and frequency >= 3 and monetary >= 3000:
            segment = "VIP"
        elif recency <= 90 and frequency >= 2:
            segment = "Loyal"
        elif recency > 180:
            segment = "At Risk"
        else:
            segment = "Regular"

        print(f"  {cid:>5} {recency:>8}d {frequency:>6} ${monetary:>10,.2f} {segment:<15}")


def product_performance_matrix(products, orders):
    """Classify products by revenue and sales volume."""
    print(f"\n{'=' * 60}")
    print("  Decision Support: Product Performance Matrix")
    print(f"{'=' * 60}")
    product_stats = defaultdict(lambda: {"revenue": 0, "units": 0})
    for o in orders:
        pid = o["product_id"]
        product_stats[pid]["revenue"] += o["line_total"]
        product_stats[pid]["units"] += o["quantity"]

    product_map = {p["product_id"]: p["product_name"] for p in products}
    avg_rev = mean([s["revenue"] for s in product_stats.values()])
    avg_units = mean([s["units"] for s in product_stats.values()])

    print(f"  Avg Revenue: ${avg_rev:,.2f}  |  Avg Units: {avg_units:.1f}")
    print(f"\n  {'Product':<25} {'Revenue':>12} {'Units':>7} {'Class':<12}")
    print(f"  {'-' * 25} {'-' * 12} {'-' * 7} {'-' * 12}")

    for pid in sorted(product_stats):
        s = product_stats[pid]
        name = product_map.get(pid, f"Product {pid}")
        if s["revenue"] >= avg_rev and s["units"] >= avg_units:
            cls = "* Star"
        elif s["revenue"] >= avg_rev:
            cls = "Cash Cow"
        elif s["units"] >= avg_units:
            cls = "Volume Play"
        else:
            cls = "Niche"

        print(f"  {name:<25} ${s['revenue']:>10,.2f} {s['units']:>7} {cls:<12}")


# ============================================================
# SECTION 8: CSV FILE PROCESSING UTILITIES
# ============================================================

def read_csv_file(filepath):
    """Read a CSV file and return a list of dictionaries."""
    if not os.path.exists(filepath):
        print(f"  File not found: {filepath}")
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_csv_file(filepath, rows, fieldnames=None):
    """Write a list of dicts to a CSV file."""
    if not rows:
        return
    fields = fieldnames or list(rows[0].keys())
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Wrote {len(rows)} rows to {filepath}")


def csv_column_stats(rows, column):
    """Compute stats for a numeric column in CSV data."""
    values = []
    null_count = 0
    for row in rows:
        val = row.get(column)
        if val is None or val == "":
            null_count += 1
        else:
            try:
                values.append(float(val))
            except ValueError:
                pass
    print(f"\n  Column: {column}")
    print(f"    Non-null: {len(values)}  |  Null: {null_count}")
    if values:
        print(f"    Mean: {mean(values):,.2f}  |  Median: {median(values):,.2f}")
        print(f"    Min:  {min(values):,.2f}  |  Max:    {max(values):,.2f}")
    return values


# ============================================================
# MAIN -- Run the complete analytics pipeline
# ============================================================

def main():
    print("+" + "=" * 58 + "+")
    print("|  FLLC Enterprise -- Data Analytics Pipeline             |")
    print("|  CIS 276DA -- Advanced SQL & Data Analytics             |")
    print("|  Author: Preston Furulie                                |")
    print("+" + "=" * 58 + "+")

    # Stage 1: ETL
    pipeline = ETLPipeline()
    pipeline.extract().transform().load()

    products = pipeline.clean_products
    orders = pipeline.clean_orders

    # Stage 2: Statistical Analysis
    print("\n\n" + "=" * 60)
    print("STATISTICAL ANALYSIS")
    print("=" * 60)

    list_prices = [p["list_price"] for p in products]
    sale_prices = [p["sale_price"] for p in products]
    order_totals = [o["line_total"] for o in orders]

    statistical_summary("Product List Prices", list_prices)
    statistical_summary("Product Sale Prices", sale_prices)
    statistical_summary("Order Line Totals", order_totals)

    # Stage 3: Visualization
    print("\n\n" + "=" * 60)
    print("DATA VISUALIZATION")
    print("=" * 60)

    cat_labels = sorted(set(p["category"] for p in products))
    cat_revenues = []
    for cat in cat_labels:
        cat_product_ids = {p["product_id"] for p in products
                          if p["category"] == cat}
        rev = sum(o["line_total"] for o in orders
                  if o["product_id"] in cat_product_ids)
        cat_revenues.append(rev)
    horizontal_bar_chart("Revenue by Category", cat_labels, cat_revenues)

    histogram("Product Price Distribution", list_prices, bins=6)

    # Stage 4: Aggregation
    print("\n\n" + "=" * 60)
    print("AGGREGATION & GROUPING")
    print("=" * 60)
    aggregate_by_category(products)
    month_labels, month_values = aggregate_by_month(orders)

    # Stage 5: Trend Analysis
    print("\n\n" + "=" * 60)
    print("TREND ANALYSIS")
    print("=" * 60)
    trend_analysis(month_labels, month_values, window=3)
    month_over_month_growth(month_labels, month_values)

    # Stage 6: Normalization
    print("\n\n" + "=" * 60)
    print("DATA NORMALIZATION")
    print("=" * 60)
    demonstrate_normalization(products)

    # Stage 7: Decision Support
    print("\n\n" + "=" * 60)
    print("DECISION SUPPORT")
    print("=" * 60)
    customer_rfm_analysis(orders)
    product_performance_matrix(products, orders)

    print("\n" + "+" + "=" * 58 + "+")
    print("|  Pipeline complete -- all stages executed successfully  |")
    print("+" + "=" * 58 + "+")


if __name__ == "__main__":
    main()
