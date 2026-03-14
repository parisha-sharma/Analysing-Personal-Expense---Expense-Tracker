import pandas as pd
from db_config import get_connection

# -----------------------------
# COMMON EXECUTION FUNCTION
# -----------------------------
def run(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# -----------------------------
# SUMMARY
# -----------------------------
def summary():
    return run("""
        SELECT COUNT(*) AS total_transactions,
               SUM(amount_paid) AS total_spent,
               SUM(cashback) AS total_cashback,
               AVG(amount_paid) AS avg_transaction
        FROM expenses
    """)


# -----------------------------
# CORE 15 QUERIES
# -----------------------------
core_queries = {

"Total Spent by Category (in Rs)":
"""SELECT category, SUM(amount_paid) AS total_spent
   FROM expenses GROUP BY category ORDER BY total_spent DESC""",

"Total Spent by Payment Mode":
"""SELECT payment_mode, SUM(amount_paid) AS total_spent
   FROM expenses GROUP BY payment_mode""",

"Monthly Spending":
"""SELECT MONTH(date) AS month, SUM(amount_paid) AS total_spent
   FROM expenses GROUP BY month ORDER BY month""",

"Cashback by Category":
"""SELECT category, SUM(cashback) AS total_cashback
   FROM expenses GROUP BY category""",

"Top 5 Transactions":
"""SELECT date, category, amount_paid
   FROM expenses ORDER BY amount_paid DESC LIMIT 5""",

"Weekday vs Weekend":
"""SELECT CASE WHEN DAYOFWEEK(date) IN (1,7)
       THEN 'Weekend' ELSE 'Weekday' END AS day_type,
       SUM(amount_paid) AS total_spent
       FROM expenses GROUP BY day_type""",

"Quarterly Spending":
"""SELECT QUARTER(date) AS quarter, SUM(amount_paid) AS total_spent
   FROM expenses GROUP BY quarter ORDER BY quarter""",

"Highest Spending Month":
"""SELECT MONTH(date) AS month, SUM(amount_paid) AS total_spent
   FROM expenses GROUP BY month ORDER BY total_spent DESC LIMIT 1""",

"Lowest Spending Month":
"""SELECT MONTH(date) AS month, SUM(amount_paid) AS total_spent
   FROM expenses GROUP BY month ORDER BY total_spent ASC LIMIT 1""",

"Average by Category":
"""SELECT category, AVG(amount_paid) AS avg_spent
   FROM expenses GROUP BY category""",

"Cashback Transactions":
"""SELECT * FROM expenses WHERE cashback > 0""",

"Above Average Transactions":
"""SELECT * FROM expenses
   WHERE amount_paid > (SELECT AVG(amount_paid) FROM expenses)""",

"Top Category Share (%)":
"""SELECT category,
       ROUND(SUM(amount_paid) /
       (SELECT SUM(amount_paid) FROM expenses) * 100,2) AS percentage
       FROM expenses GROUP BY category
       ORDER BY percentage DESC LIMIT 1""",

"Payment Mode Cashback":
"""SELECT payment_mode, SUM(cashback) AS total_cashback
   FROM expenses GROUP BY payment_mode""",

"Transactions Per Category":
"""SELECT category, COUNT(*) AS total_transactions
   FROM expenses GROUP BY category"""
}


# -----------------------------
# ADVANCED 15 QUERIES
# -----------------------------
advanced_queries = {

"Daily Average per Month":
"""SELECT MONTH(date) AS month,
       AVG(amount_paid) AS daily_avg
   FROM expenses GROUP BY month ORDER BY month""",

"Max Transaction per Category":
"""SELECT category, MAX(amount_paid) AS max_spent
   FROM expenses GROUP BY category""",

"Min Transaction per Category":
"""SELECT category, MIN(amount_paid) AS min_spent
   FROM expenses GROUP BY category""",

"Total Cashback Percentage (%)":
"""SELECT ROUND(SUM(cashback) /
   SUM(amount_paid) * 100,2) AS cashback_percent
   FROM expenses""",

"Spending Trend by Year":
"""SELECT YEAR(date) AS year,
   SUM(amount_paid) AS total_spent
   FROM expenses GROUP BY year""",

"Weekend Average":
"""SELECT AVG(amount_paid) AS avg_weekend
   FROM expenses WHERE DAYOFWEEK(date) IN (1,7)""",

"Weekday Average":
"""SELECT AVG(amount_paid) AS avg_weekday
   FROM expenses WHERE DAYOFWEEK(date) NOT IN (1,7)""",

"Top 3 Categories":
"""SELECT category, SUM(amount_paid) AS total_spent
   FROM expenses GROUP BY category
   ORDER BY total_spent DESC LIMIT 3""",

"Transactions with No Cashback":
"""SELECT COUNT(*) AS total_no_cashback
   FROM expenses WHERE cashback = 0""",

"Highest Cashback Transaction":
"""SELECT * FROM expenses
   ORDER BY cashback DESC LIMIT 1""",

"Payment Mode Efficiency Ratio (%)":
"""SELECT 
payment_mode,
ROUND(SUM(cashback) / SUM(amount_paid) * 100, 2) AS cashback_efficiency_percent
FROM expenses
GROUP BY payment_mode""",

"Spending Distribution":
"""SELECT FLOOR(amount_paid/500)*500 AS range_start,
   COUNT(*) AS frequency
   FROM expenses GROUP BY range_start""",

"Most Used Payment Mode":
"""SELECT payment_mode, COUNT(*) AS total
   FROM expenses GROUP BY payment_mode
   ORDER BY total DESC LIMIT 1""",

"Monthly Cashback":
"""SELECT MONTH(date) AS month,
   SUM(cashback) AS total_cashback
   FROM expenses GROUP BY month ORDER BY month""",

"High-Value Transaction Ratio (%)":
"""SELECT 
ROUND(
    SUM(CASE 
        WHEN amount_paid > (SELECT AVG(amount_paid) FROM expenses)
        THEN 1 ELSE 0 END
    ) / COUNT(*) * 100, 2
) AS high_value_percent
FROM expenses"""
}