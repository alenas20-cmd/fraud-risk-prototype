# fraud_risk/config.py

# Risk thresholds
LOW_RISK_THRESHOLD = 30
MEDIUM_RISK_THRESHOLD = 70

# Scoring settings
BASE_SCORE_MULTIPLIER = 0.02

# High amount trigger
HIGH_AMOUNT_LIMIT = 3000
HIGH_AMOUNT_BONUS = 20
# Rule weights (points)
NIGHT_TIME_BONUS = 15
NEW_CUSTOMER_BONUS = 15
NON_UA_COUNTRY_BONUS = 20
REASON_DESCRIPTIONS = {
    "BASE_AMOUNT": "Base score from transaction amount",
    "HIGH_AMOUNT": "Transaction amount is above high-amount limit",
    "NIGHT_TIME": "Transaction made at night (00:00–05:59)",
    "NEW_CUSTOMER": "Customer is new",
    "NON_UA_COUNTRY": "Transaction country is not UA",
}