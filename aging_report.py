from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Iterable

from demo_data import Transaction, build_demo_data


@dataclass(frozen=True)
class AgingBucket:
    key: str
    label: str
    amount: Decimal
    document_count: int


_BUCKETS: tuple[tuple[str, str], ...] = (
    ("overdue_61_plus", "61+ gün gecikmiş"),
    ("overdue_31_60", "31-60 gün gecikmiş"),
    ("overdue_8_30", "8-30 gün gecikmiş"),
    ("overdue_1_7", "1-7 gün gecikmiş"),
    ("due_today", "Bugün vadeli"),
    ("due_1_7", "1-7 gün içinde"),
    ("due_8_30", "8-30 gün içinde"),
    ("due_31_plus", "31+ gün içinde"),
)


def _bucket_key(days_to_due: int) -> str:
    if days_to_due <= -61:
        return "overdue_61_plus"
    if days_to_due <= -31:
        return "overdue_31_60"
    if days_to_due <= -8:
        return "overdue_8_30"
    if days_to_due <= -1:
        return "overdue_1_7"
    if days_to_due == 0:
        return "due_today"
    if days_to_due <= 7:
        return "due_1_7"
    if days_to_due <= 30:
        return "due_8_30"
    return "due_31_plus"


def build_aging_report(
    transactions: Iterable[Transaction],
    *,
    as_of: date | None = None,
) -> list[AgingBucket]:
    """Group open, due-dated synthetic transactions into deterministic aging buckets."""
    report_date = as_of or date.today()
    totals = {key: Decimal("0") for key, _ in _BUCKETS}
    counts = {key: 0 for key, _ in _BUCKETS}

    for transaction in transactions:
        if transaction.status.casefold() in {"tamamlandı", "kapalı", "iptal"}:
            continue
        if transaction.due_date is None:
            continue
        key = _bucket_key((transaction.due_date - report_date).days)
        totals[key] += transaction.amount
        counts[key] += 1

    return [
        AgingBucket(key=key, label=label, amount=totals[key], document_count=counts[key])
        for key, label in _BUCKETS
    ]


def format_try(value: Decimal) -> str:
    text = f"{value:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return f"₺{text}"


def main() -> int:
    data = build_demo_data()
    report_date = data["generated_on"]
    transactions = data["transactions"]
    if not isinstance(report_date, date) or not isinstance(transactions, list):
        raise TypeError("Demo veri yapısı beklenen formatta değil.")

    print(f"Cari yaşlandırma özeti — {report_date:%d.%m.%Y}")
    print("-" * 58)
    for bucket in build_aging_report(transactions, as_of=report_date):
        print(f"{bucket.label:<23} {bucket.document_count:>3} belge  {format_try(bucket.amount):>18}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
