from fraud_risk.db import create_tables, insert_sample_data, print_summary_report
from fraud_risk.model import run_demo


def main() -> None:
    print("Fraud Risk Prototype started")
    create_tables()
    insert_sample_data()

    run_demo()
    print_summary_report()


if __name__ == "__main__":
    main()
