from fraud_risk.data_prep import load_data
from fraud_risk.config import (
    LOW_RISK_THRESHOLD,
    MEDIUM_RISK_THRESHOLD,
    BASE_SCORE_MULTIPLIER,
    HIGH_AMOUNT_LIMIT,
    HIGH_AMOUNT_BONUS,
    NIGHT_TIME_BONUS,
    NEW_CUSTOMER_BONUS,
    NON_UA_COUNTRY_BONUS,
    REASON_DESCRIPTIONS,
)
from fraud_risk.db import update_transaction_result


def risk_bucket(score: int) -> str:
    if score >= MEDIUM_RISK_THRESHOLD:
        return "HIGH"
    if score >= LOW_RISK_THRESHOLD:
        return "MEDIUM"
    return "LOW"


def score_transaction(txn: dict) -> tuple[int, str, list[str]]:
    amount = float(txn["amount"])
    hour = int(txn["hour"])
    is_new = bool(txn["is_new_customer"])
    country = str(txn["country"])

    reasons: list[str] = []

    # Base score from amount
    score = int(amount * BASE_SCORE_MULTIPLIER)
    reasons.append("BASE_AMOUNT")

    # Rule 1: high amount
    if amount > HIGH_AMOUNT_LIMIT:
        score += HIGH_AMOUNT_BONUS
        reasons.append("HIGH_AMOUNT")

    # Rule 2: night time (00-05)
    if 0 <= hour <= 5:
        score += NIGHT_TIME_BONUS
        reasons.append("NIGHT_TIME")

    # Rule 3: new customer
    if is_new:
        score += NEW_CUSTOMER_BONUS
        reasons.append("NEW_CUSTOMER")

    # Rule 4: non-UA country (demo)
    if country != "UA":
        score += NON_UA_COUNTRY_BONUS
        reasons.append("NON_UA_COUNTRY")

    if score > 100:
        score = 100

    bucket = risk_bucket(score)
    return score, bucket, reasons


def run_demo() -> None:
    print("🤖 Running fraud risk model...")

    transactions = load_data()

    print("\nRisk evaluation results:")
    for txn in transactions:
        score, bucket, reasons = score_transaction(txn)

        # ✅ persist results to SQLite
        update_transaction_result(txn["txn_id"], score, bucket)

        print(
            f"{txn['txn_id']}: amount={txn['amount']} "
            f"score={score:3d} bucket={bucket} "
            f"reasons={reasons}"
        )

        reason_texts = [REASON_DESCRIPTIONS[r] for r in reasons]
        print("   → " + "; ".join(reason_texts))