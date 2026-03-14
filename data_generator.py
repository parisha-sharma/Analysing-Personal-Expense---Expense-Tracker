import random
from faker import Faker
from datetime import datetime, timedelta
from db_config import get_connection

fake = Faker()

# ----------------------------------------
# CONFIGURATION
# ----------------------------------------
TOTAL_RECORDS = 300
START_YEAR = 2025

CATEGORIES = [
    "Groceries", "Food", "Transport", "Travel",
    "Entertainment", "Shopping", "Bills",
    "Healthcare", "Education", "Subscriptions"
]

PAYMENT_MODES = [
    "Cash", "UPI", "Debit Card", "Credit Card"
]


# ----------------------------------------
# CREATE TABLE IF NOT EXISTS
# ----------------------------------------
def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    create_query = """
    CREATE TABLE IF NOT EXISTS expenses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date DATE,
        category VARCHAR(100),
        payment_mode VARCHAR(50),
        description VARCHAR(255),
        amount_paid DECIMAL(10,2),
        cashback DECIMAL(10,2)
    );
    """

    cursor.execute(create_query)
    connection.commit()
    cursor.close()
    connection.close()


# ----------------------------------------
# GENERATE RANDOM DATE ACROSS 12 MONTHS
# ----------------------------------------
def random_date():
    start_date = datetime(START_YEAR, 1, 1)
    end_date = datetime(START_YEAR, 12, 31)

    random_days = random.randint(0, (end_date - start_date).days)
    return start_date + timedelta(days=random_days)


# ----------------------------------------
# GENERATE DATA
# ----------------------------------------
def generate_data():
    data = []

    for _ in range(TOTAL_RECORDS):
        date = random_date().date()
        category = random.choice(CATEGORIES)
        payment_mode = random.choice(PAYMENT_MODES)
        description = fake.sentence(nb_words=5)

        amount = round(random.uniform(100, 5000), 2)

        # 30% chance of cashback
        cashback = round(amount * random.uniform(0.01, 0.1), 2) if random.random() < 0.3 else 0.00

        data.append((date, category, payment_mode, description, amount, cashback))

    return data


# ----------------------------------------
# INSERT DATA INTO DATABASE
# ----------------------------------------
def insert_data(data):
    connection = get_connection()
    cursor = connection.cursor()

    insert_query = """
    INSERT INTO expenses (date, category, payment_mode, description, amount_paid, cashback)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.executemany(insert_query, data)
    connection.commit()

    cursor.close()
    connection.close()


# ----------------------------------------
# MAIN EXECUTION
# ----------------------------------------
if __name__ == "__main__":
    print("Creating table if not exists...")
    create_table()

    print("Generating fake expense data...")
    data = generate_data()

    print("Inserting data into database...")
    insert_data(data)

    print("✅ 300 records successfully inserted into expense_tracker.expenses")