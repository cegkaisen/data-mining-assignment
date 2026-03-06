## **1. Introduction**

Git repository link: https://github.com/cegkaisen/data-mining-assignment

In this study, I performed association rule mining on the provided grocery shopping dataset. Association rule mining is a data mining method used to identify frequently co-occurring items within transaction data and the relationships between them. This method is particularly used for market basket analysis. It allows us to examine which product categories are purchased together in customers' shopping baskets.

I applied the necessary preprocessing steps on the dataset, created transactions, and extracted frequent itemsets and association rules using the Apriori algorithm. I also examined the effect of these parameters on the results by testing different support and confidence values.

Note: I used an AI-powered tool during the code development process.

Note 2: I moved the .csv files into the data folder; the same must be done for the code to work.

## **2. Dataset Description**

Tables and descriptions in the data set used:
- orders.csv: It contains order information for each order. For example, order_id, order_dow, and order_hour_of_day.

- order_products.csv: 
It shows which products are included in which order.

- products.csv: 
It includes product names and product categories.

- aisles.csv: 
Matches products with aisle categories.

- departments.csv: 
It includes more general product categories.

The original dataset contains approximately 3.4 million orders. Since association rule mining algorithms are quite costly on large datasets, I used a random sample of 50,000 orders for the analysis.

```python
sample_size = 50000

sampled_orders = orders.sample(n=sample_size, random_state=42)
```

## **3. Data Preparation**

In the analysis, each order has been treated as a transaction.

Instead of using `product_id` directly as an item, I used `aisle` categories. Aisle categories are more interpretable, and using aisles makes the analysis more manageable by reducing the number of items.

I followed these steps during the data preparation process:

1. I randomly selected 50,000 orders from the orders table.

2. I filtered the order_products table to include only the records belonging to these orders.

3. I added the product information from the products table.

4. I joined the aisle categories with the aisles table.

5. I grouped the data to create a transaction for each order_id.

6. I removed duplicate aisle values within the same transaction.

7. As a result of these operations, I converted each transaction into a list consisting of unique aisle categories within an order.

An example from the table generated as a result of these operations:

```
393 -> [breakfast bars pastries, candy chocolate, fresh fruits, milk, packaged cheese, packaged produce]

```

## **4. Frequent Itemset Mining**

I used the `Apriori` algorithm to find frequent itemsets.

To apply the Apriori algorithm, I first converted the transaction data into one-hot encoded format. I used TransactionEncoder for this process. In this format, each column represents an aisle category and contains binary values indicating whether this category is present or absent for each transaction.

Then, using the Apriori algorithm, itemsets exceeding the minimum support value were identified.

## **5. Threshold Analysis**

Association rule mining results are highly sensitive to the selected support and confidence values. Therefore, I examined how the results changed by testing different threshold values.

I observed that the number of itemsets and rules found increased rapidly when the support value was reduced.

| min_support | frequent itemsets | rules |
|-------------|-------------------|-------|
| 0.02        | 420               | 266   |
| 0.01        | 930               | 378   |
| 0.005       | 1747              | 459   |

Similarly, as the confidence value increases, the number of rules decreases.

| min_support | rules |
|-------------|-------|
| 0.2         | 9753  |
| 0.3         | 6796  |
| 0.5         | 3647  |
| 0.7         | 1598  |

Higher confidence values produce more reliable rules while reducing the total number of rules.

## **6. Association Rules and Insights**

As a result of the a priori analysis, I obtained several meaningful association rules.

### **Rule 1**

**pasta sauce → dry pasta**

- support: 0.0196

- confidence: 0.3139

- lift: 4.45

This rule has a high lift value and indicates a strong complementary product relationship. Customers who purchase pasta sauce are much more likely than average to purchase dry pasta. It can be used for cross-selling strategies.

### **Rule 2**

**granola → yogurt**

- support: 0.0157

- confidence: 0.5499
  
- lift: 2.10

This rule indicates that granola and yogurt products are frequently purchased together. The high confidence value indicates that approximately half of customers who purchase granola also purchase yogurt. This may particularly reflect breakfast or healthy snack consumption habits.

### **Rule 3**

**fresh herbs → fresh vegetables**

- support: 0.0778

- confidence: 0.8399
  
- lift: 1.89

This rule has a very high confidence value. The vast majority of customers who purchase fresh herbs also purchase fresh vegetables. This indicates that customers purchase these products together for meal preparation.

### **Rule 4**

**fresh fruits → fresh vegetables**

- support: 0.3175

- confidence: 0.5709
  
- lift: 1.28

This rule is one of the rules with the highest support value. This indicates that customers frequently purchase fruit and vegetable categories together during their shopping. Although the lift value is not very high, the high support value indicates that this relationship is a fairly common shopping behavior.


## **7. Time-based Pattern Analysis**

I examined whether the timing of purchases also affects transaction behavior, in addition to the relationships between product categories. For this purpose, the time period when the order was placed was also added as an item to each transaction.

The `order_hour_of_day` variable has been divided into four time categories to enable more meaningful analysis:

- morning

- afternoon

- evening

- night

After this process, I recreated the transaction lists to include both product categories and purchase times. Example transaction:

```
[fresh fruits, yogurt, milk, morning]
```

When I reran the Apriori algorithm, I noticed that some rules appeared in conjunction with specific time periods. For example, the following rule is noteworthy:

Rule: 
```
{pasta sauce, afternoon} → {dry pasta}

- support: 0.0106
- confidence: 0.3333
- lift: 4.73
```

This rule has a high lift value. This result indicates that customers who purchase pasta sauce in the afternoon are more likely to purchase dry pasta. This can be explained by customers shopping for meal preparation.

Additionally, in some rules, it has been observed that the afternoon time period coincides with products such as fresh vegetables and packaged cheese. This indicates that customers tend to purchase the necessary products for meals together during these hours.

These results indicate that shopping time can also influence customer behavior. Such information could be useful for time-aware recommendation systems.


## **8. Conclusion**

In this study, I applied association rule mining on grocery transaction data. Using the Apriori algorithm, I identified frequently purchased product categories.

The rules obtained reveal meaningful insights into customers' shopping behavior. In particular, a clear tendency to purchase certain product categories together has been observed. Furthermore, the short time-based analysis conducted suggests that shopping time may also be related to certain product combinations.

These types of analyses can be useful for developing store layouts, cross-selling strategies, and recommendation systems.
