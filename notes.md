**Task 1 notes**

The dataset consists of five related CSV files: orders, order_products, products, aisles, and departments.

orders contains order-level metadata such as order_dow and order_hour_of_day.

order_products links each order_id to purchased product_ids.

products maps products to aisle_id and department_id.

For this assignment, transactions are defined at the order level, meaning each order_id is one transaction.

We chose to analyze items at the aisle level rather than product level, because aisle categories are more interpretable and produce more meaningful support values.

Since the full dataset is very large, we applied random order sampling and selected 50,000 orders.

We then filtered order_products to only keep products belonging to sampled orders.

The sampled product records were joined with products and aisles to obtain aisle labels.

Finally, transactions were built by grouping rows by order_id and collecting aisle names.

A necessary preprocessing step is to remove duplicate aisle entries within the same transaction, since association rule mining should treat items as present/absent within a basket.