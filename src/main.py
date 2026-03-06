from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

orders_path = DATA_DIR / "orders.csv"
order_products_path = DATA_DIR / "order_products.csv"
products_path = DATA_DIR / "products.csv"
aisles_path = DATA_DIR / "aisles.csv"
departments_path = DATA_DIR / "departments.csv"

print("Base directory:", BASE_DIR)
print("Data directory:", DATA_DIR)
print("Loading datasets...")

orders = pd.read_csv(orders_path)
products = pd.read_csv(products_path)
aisles = pd.read_csv(aisles_path)
departments = pd.read_csv(departments_path)

# Large file: load only a preview first
order_products_preview = pd.read_csv(order_products_path, nrows=10)

print("\n=== ORDERS ===")
print(orders.head())
print("\nColumns:", list(orders.columns))
print("Shape:", orders.shape)

print("\n=== ORDER_PRODUCTS (preview) ===")
print(order_products_preview.head())
print("\nColumns:", list(order_products_preview.columns))
print("Preview shape:", order_products_preview.shape)

print("\n=== PRODUCTS ===")
print(products.head())
print("\nColumns:", list(products.columns))
print("Shape:", products.shape)

print("\n=== AISLES ===")
print(aisles.head())
print("\nColumns:", list(aisles.columns))
print("Shape:", aisles.shape)

print("\n=== DEPARTMENTS ===")
print(departments.head())
print("\nColumns:", list(departments.columns))
print("Shape:", departments.shape)

#################################################################################

print("\n=== SAMPLING ORDERS ===")

sample_size = 50000

sampled_orders = orders.sample(n=sample_size, random_state=42)

print("Sampled orders:", sampled_orders.shape)

sampled_order_ids = set(sampled_orders["order_id"])

print("\n=== LOADING ORDER_PRODUCTS SUBSET ===")

order_products = pd.read_csv(order_products_path)

order_products_subset = order_products[
    order_products["order_id"].isin(sampled_order_ids)
]

print("Filtered order_products:", order_products_subset.shape)


##################################################################3

print("\n=== JOIN PRODUCTS ===")

order_products_subset = order_products_subset.merge(
    products,
    on="product_id"
)

print(order_products_subset.head())

print("\n=== JOIN AISLES ===")

order_products_subset = order_products_subset.merge(
    aisles,
    on="aisle_id"
)

print(order_products_subset.head())

#####################################################################

print("\n=== BUILDING TRANSACTIONS ===")

transactions = order_products_subset.groupby("order_id")["aisle"].apply(list)

print(transactions.head())
print("Total transactions:", len(transactions))

##############################################################

print(transactions.iloc[0])