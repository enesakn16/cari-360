from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal


@dataclass(frozen=True)
class Supplier:
    code: str
    name: str
    balance: Decimal
    overdue: Decimal
    next_due: date
    currency: str = "TRY"


@dataclass(frozen=True)
class Customer:
    code: str
    name: str
    balance: Decimal
    credit_limit: Decimal
    status: str


@dataclass(frozen=True)
class Transaction:
    document_no: str
    party: str
    kind: str
    amount: Decimal
    transaction_date: date
    due_date: date | None
    status: str


@dataclass(frozen=True)
class CashAccount:
    name: str
    account_type: str
    balance: Decimal


def build_demo_data() -> dict[str, object]:
    """Return synthetic records only. No values originate from production."""
    today = date.today()
    suppliers = [
        Supplier("T-1001", "Atlas Yedek Parça", Decimal("184250.00"), Decimal("22500.00"), today + timedelta(days=3)),
        Supplier("T-1002", "Mavi Rota Dağıtım", Decimal("96780.50"), Decimal("0"), today + timedelta(days=8)),
        Supplier("T-1003", "Nova Endüstri", Decimal("73120.00"), Decimal("8400.00"), today - timedelta(days=2)),
        Supplier("T-1004", "Kuzey Ticaret", Decimal("41350.75"), Decimal("0"), today + timedelta(days=14)),
        Supplier("T-1005", "Pera Ekipman", Decimal("28990.00"), Decimal("0"), today + timedelta(days=21)),
    ]
    customers = [
        Customer("M-2001", "Örnek Servis A.Ş.", Decimal("76400.00"), Decimal("150000.00"), "Normal"),
        Customer("M-2002", "Demo Motor Ltd.", Decimal("45950.25"), Decimal("80000.00"), "Normal"),
        Customer("M-2003", "Kent Atölye", Decimal("21980.00"), Decimal("25000.00"), "Limite Yakın"),
        Customer("M-2004", "Rota Teknik", Decimal("12400.00"), Decimal("60000.00"), "Normal"),
        Customer("M-2005", "Pilot Garaj", Decimal("0"), Decimal("30000.00"), "Temiz"),
    ]
    transactions = [
        Transaction("FTR-2026-041", "Atlas Yedek Parça", "Alış Faturası", Decimal("48500"), today - timedelta(days=23), today - timedelta(days=2), "Gecikmiş"),
        Transaction("FTR-2026-057", "Mavi Rota Dağıtım", "Alış Faturası", Decimal("32200"), today - timedelta(days=16), today + timedelta(days=8), "Açık"),
        Transaction("SAT-2026-188", "Örnek Servis A.Ş.", "Satış", Decimal("18900"), today - timedelta(days=4), today + timedelta(days=26), "Açık"),
        Transaction("SAT-2026-193", "Demo Motor Ltd.", "Satış", Decimal("12750"), today - timedelta(days=2), today + timedelta(days=28), "Açık"),
        Transaction("THS-2026-066", "Kent Atölye", "Tahsilat", Decimal("8500"), today - timedelta(days=1), None, "Tamamlandı"),
        Transaction("ODM-2026-029", "Nova Endüstri", "Ödeme", Decimal("15000"), today, None, "Tamamlandı"),
    ]
    cash_accounts = [
        CashAccount("Ana Kasa", "Nakit", Decimal("58420.00")),
        CashAccount("Banka Hesabı", "Banka", Decimal("217890.25")),
        CashAccount("Kredi Kartı POS", "POS", Decimal("94250.00")),
        CashAccount("Online Tahsilat", "Sanal POS", Decimal("36780.50")),
    ]
    monthly_sales = [118_000, 136_500, 129_400, 157_200, 171_800, 189_600, 204_300, 221_900, 213_500, 248_700, 265_400, 286_900]
    return {
        "suppliers": suppliers,
        "customers": customers,
        "transactions": transactions,
        "cash_accounts": cash_accounts,
        "monthly_sales": monthly_sales,
        "generated_on": today,
    }
