from datetime import date, timedelta
from decimal import Decimal

from aging_report import build_aging_report, format_try
from demo_data import Transaction


def transaction(
    document_no: str,
    *,
    amount: str,
    days_to_due: int | None,
    status: str = "Açık",
) -> Transaction:
    report_date = date(2026, 8, 5)
    return Transaction(
        document_no=document_no,
        party="Sentetik Cari",
        kind="Alış Faturası",
        amount=Decimal(amount),
        transaction_date=report_date - timedelta(days=10),
        due_date=None if days_to_due is None else report_date + timedelta(days=days_to_due),
        status=status,
    )


def as_map(rows):
    return {row.key: row for row in rows}


def test_groups_open_documents_into_expected_buckets():
    report_date = date(2026, 8, 5)
    rows = build_aging_report(
        [
            transaction("A", amount="100", days_to_due=-75),
            transaction("B", amount="200", days_to_due=-31),
            transaction("C", amount="300", days_to_due=-8),
            transaction("D", amount="400", days_to_due=-1),
            transaction("E", amount="500", days_to_due=0),
            transaction("F", amount="600", days_to_due=7),
            transaction("G", amount="700", days_to_due=30),
            transaction("H", amount="800", days_to_due=31),
        ],
        as_of=report_date,
    )
    buckets = as_map(rows)

    assert buckets["overdue_61_plus"].amount == Decimal("100")
    assert buckets["overdue_31_60"].amount == Decimal("200")
    assert buckets["overdue_8_30"].amount == Decimal("300")
    assert buckets["overdue_1_7"].amount == Decimal("400")
    assert buckets["due_today"].amount == Decimal("500")
    assert buckets["due_1_7"].amount == Decimal("600")
    assert buckets["due_8_30"].amount == Decimal("700")
    assert buckets["due_31_plus"].amount == Decimal("800")
    assert all(bucket.document_count == 1 for bucket in rows)


def test_ignores_completed_and_undated_transactions():
    rows = build_aging_report(
        [
            transaction("DONE", amount="900", days_to_due=-5, status="Tamamlandı"),
            transaction("NO-DUE", amount="500", days_to_due=None),
            transaction("OPEN", amount="125", days_to_due=3),
        ],
        as_of=date(2026, 8, 5),
    )
    buckets = as_map(rows)

    assert sum((row.amount for row in rows), Decimal("0")) == Decimal("125")
    assert sum(row.document_count for row in rows) == 1
    assert buckets["due_1_7"].amount == Decimal("125")


def test_aggregates_multiple_documents_without_float_rounding():
    rows = build_aging_report(
        [
            transaction("A", amount="10.10", days_to_due=-2),
            transaction("B", amount="20.20", days_to_due=-3),
        ],
        as_of=date(2026, 8, 5),
    )
    bucket = as_map(rows)["overdue_1_7"]

    assert bucket.amount == Decimal("30.30")
    assert bucket.document_count == 2
    assert format_try(bucket.amount) == "₺30,30"
