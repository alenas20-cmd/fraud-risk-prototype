# Fraud Risk Prototype (Python + SQL)

This is a mini fraud-risk scoring system built with Python and SQLite.

The project demonstrates how transaction data can be stored, processed, scored, and analyzed using rule-based risk logic.

---

## What the Project Does

- Stores transactions and customers in a SQLite database
- Loads data using SQL (including JOIN)
- Applies rule-based fraud scoring
- Assigns a risk bucket (LOW / MEDIUM / HIGH)
- Provides explainable reasons for each decision
- Writes scoring results back to the database
- Generates a simple SQL analytics summary

---

## Project Structure

- `analysis.py` – entry point that runs the full pipeline
- `src/fraud_risk/db.py` – database schema, sample data, updates, summary queries
- `src/fraud_risk/data_prep.py` – SQL data loading
- `src/fraud_risk/model.py` – scoring rules and risk logic
- `src/fraud_risk/config.py` – thresholds, weights, reason descriptions
- `fraud.db` – generated SQLite database

---

## Risk Scoring Logic

Risk score is calculated using:

- Base score from transaction amount
- High amount bonus
- Night-time transaction bonus (00:00–05:59)
- New customer bonus
- Non-UA country bonus

Risk buckets:

- LOW: score < 30
- MEDIUM: 30–69
- HIGH: 70+

Each transaction includes explainable reason codes.

---

## How to Run

```bash
python analysis.py