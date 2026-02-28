import sqlite3


DB_NAME = "fraud.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables() -> None:
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id TEXT PRIMARY KEY,
                country TEXT,
                is_new_customer INTEGER
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                txn_id TEXT PRIMARY KEY,
                customer_id TEXT,
                amount REAL,
                hour INTEGER,
                score INTEGER,
                bucket TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
            )
        """)

        conn.commit()


def insert_sample_data() -> None:
    with get_connection() as conn:
        cursor = conn.cursor()

        # Clear old data
        cursor.execute("DELETE FROM transactions")
        cursor.execute("DELETE FROM customers")

        # Insert customers
        customers = [
            ("C1", "UA", 0),
            ("C2", "UA", 1),
            ("C3", "PL", 0),
            ("C4", "US", 1),
        ]

        cursor.executemany("""
            INSERT INTO customers (customer_id, country, is_new_customer)
            VALUES (?, ?, ?)
        """, customers)

        # Insert transactions
        transactions = [
            ("T1", "C1", 100, 14, None, None),
            ("T2", "C2", 2500, 2, None, None),
            ("T3", "C3", 75, 10, None, None),
            ("T4", "C4", 4000, 1, None, None),
        ]

        cursor.executemany("""
            INSERT INTO transactions (txn_id, customer_id, amount, hour, score, bucket)
            VALUES (?, ?, ?, ?, ?, ?)
        """, transactions)

        conn.commit()


def update_transaction_result(txn_id: str, score: int, bucket: str) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE transactions
            SET score = ?, bucket = ?
            WHERE txn_id = ?
        """, (score, bucket, txn_id))

        conn.commit()


def print_summary_report() -> None:
    with get_connection() as conn:
        cursor = conn.cursor()

        print("\n📊 Summary report from DB:")

        # Total transactions
        cursor.execute("SELECT COUNT(*) FROM transactions")
        total = cursor.fetchone()[0]
        print(f"Total transactions in DB: {total}")

        # High risk count
        cursor.execute("SELECT COUNT(*) FROM transactions WHERE bucket = 'HIGH'")
        high_count = cursor.fetchone()[0]
        print(f"High risk transactions: {high_count}")

        # Average amount
        cursor.execute("SELECT AVG(amount) FROM transactions")
        avg_amount = cursor.fetchone()[0]
        if avg_amount is None:
            print("Average transaction amount: no data")
        else:
            print(f"Average transaction amount: {avg_amount:.2f}")

        # Average score
        cursor.execute("SELECT AVG(score) FROM transactions")
        avg_score = cursor.fetchone()[0]
        if avg_score is None:
            print("Average risk score: no data")
        else:
            print(f"Average risk score: {avg_score:.2f}")