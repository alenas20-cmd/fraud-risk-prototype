import sqlite3


def load_data() -> list[dict]:
    print("📊 Loading transaction data from DB...")

    conn = sqlite3.connect("fraud.db")
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT t.txn_id,
                          t.amount,
                          t.hour,
                          c.is_new_customer,
                          c.country
                   FROM transactions t
                            JOIN customers c ON c.customer_id = t.customer_id
                   ORDER BY t.txn_id
                   """)

    rows = cursor.fetchall()
    conn.close()

    transactions = []
    for row in rows:
        transactions.append({
            "txn_id": row[0],
            "amount": row[1],
            "hour": row[2],
            "is_new_customer": bool(row[3]),
            "country": row[4],
        })

    return transactions