from __future__ import annotations

import sys
from decimal import Decimal
from typing import Iterable, Sequence

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from demo_data import CashAccount, Customer, Supplier, Transaction, build_demo_data

APP_TITLE = "Cari 360 — Offline Demo"


def money(value: Decimal | int | float) -> str:
    amount = Decimal(str(value))
    text = f"{amount:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return f"₺{text}"


class SalesChart(QWidget):
    def __init__(self, values: Sequence[int], parent: QWidget | None = None):
        super().__init__(parent)
        self.values = list(values)
        self.setMinimumHeight(230)

    def paintEvent(self, event):  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect().adjusted(18, 18, -18, -28)
        painter.fillRect(self.rect(), QColor("#FFFFFF"))
        if not self.values:
            return
        max_value = max(self.values) * 1.12
        step_x = rect.width() / max(len(self.values) - 1, 1)
        points = []
        for index, value in enumerate(self.values):
            x = rect.left() + index * step_x
            y = rect.bottom() - (value / max_value) * rect.height()
            points.append((x, y))
        painter.setPen(QPen(QColor("#E5E7EB"), 1))
        for i in range(5):
            y = rect.top() + i * rect.height() / 4
            painter.drawLine(rect.left(), int(y), rect.right(), int(y))
        painter.setPen(QPen(QColor("#2563EB"), 3))
        for first, second in zip(points, points[1:]):
            painter.drawLine(int(first[0]), int(first[1]), int(second[0]), int(second[1]))
        painter.setBrush(QColor("#2563EB"))
        painter.setPen(Qt.PenStyle.NoPen)
        for x, y in points:
            painter.drawEllipse(int(x - 4), int(y - 4), 8, 8)
        painter.setPen(QColor("#64748B"))
        months = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"]
        for index, label in enumerate(months[: len(points)]):
            painter.drawText(int(rect.left() + index * step_x - 12), rect.bottom() + 20, 30, 16, Qt.AlignmentFlag.AlignCenter, label)


class MetricCard(QFrame):
    def __init__(self, title: str, value: str, note: str, accent: str):
        super().__init__()
        self.setObjectName("metricCard")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        top = QLabel(title)
        top.setObjectName("metricTitle")
        number = QLabel(value)
        number.setObjectName("metricValue")
        number.setStyleSheet(f"color:{accent};")
        detail = QLabel(note)
        detail.setObjectName("metricNote")
        layout.addWidget(top)
        layout.addWidget(number)
        layout.addWidget(detail)


class DataTable(QTableWidget):
    def __init__(self, headers: Sequence[str]):
        super().__init__(0, len(headers))
        self.setHorizontalHeaderLabels(list(headers))
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setShowGrid(False)

    def set_rows(self, rows: Iterable[Sequence[str]]) -> None:
        data = list(rows)
        self.setRowCount(len(data))
        for row_index, row in enumerate(data):
            for column_index, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                if column_index > 1:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
                self.setItem(row_index, column_index, item)
        self.resizeRowsToContents()


class Page(QWidget):
    def __init__(self, title: str, subtitle: str):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(26, 24, 26, 24)
        self.layout.setSpacing(16)
        heading = QLabel(title)
        heading.setObjectName("pageTitle")
        description = QLabel(subtitle)
        description.setObjectName("pageSubtitle")
        self.layout.addWidget(heading)
        self.layout.addWidget(description)


class Cari360Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = build_demo_data()
        self.setWindowTitle(APP_TITLE)
        self.setMinimumSize(QSize(1180, 760))
        self.resize(1440, 900)

        root = QWidget()
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(248)
        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(18, 24, 18, 20)
        side_layout.setSpacing(14)

        logo = QLabel("CARI 360")
        logo.setObjectName("logo")
        tagline = QLabel("Finans ve Cari Yönetimi")
        tagline.setObjectName("tagline")
        badge = QLabel("OFFLINE DEMO")
        badge.setObjectName("demoBadge")
        side_layout.addWidget(logo)
        side_layout.addWidget(tagline)
        side_layout.addWidget(badge)

        self.menu = QListWidget()
        self.menu.setObjectName("menu")
        self.menu.setSpacing(5)
        for label in ["Genel Bakış", "Tedarikçiler", "Müşteriler", "Cari Hareketler", "Kasa ve Banka", "Raporlar"]:
            QListWidgetItem(label, self.menu)
        side_layout.addWidget(self.menu, 1)

        privacy = QLabel("✓ Üretim veritabanı yok\n✓ Şube bilgisi yok\n✓ Ağ erişimi yok\n✓ Salt okunur")
        privacy.setObjectName("privacy")
        side_layout.addWidget(privacy)

        content = QFrame()
        content.setObjectName("content")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        topbar = QFrame()
        topbar.setObjectName("topbar")
        top_layout = QHBoxLayout(topbar)
        top_layout.setContentsMargins(24, 13, 24, 13)
        state = QLabel("Demo verileri · Yerel bellek · Salt okunur")
        state.setObjectName("state")
        top_layout.addWidget(state)
        top_layout.addStretch(1)
        search = QLineEdit()
        search.setPlaceholderText("Sayfada ara…")
        search.setFixedWidth(280)
        search.textChanged.connect(self.filter_current_table)
        top_layout.addWidget(search)
        close_button = QPushButton("Kapat")
        close_button.clicked.connect(self.close)
        top_layout.addWidget(close_button)
        content_layout.addWidget(topbar)

        self.stack = QStackedWidget()
        self.pages = [
            self.dashboard_page(),
            self.suppliers_page(),
            self.customers_page(),
            self.transactions_page(),
            self.finance_page(),
            self.reports_page(),
        ]
        for page in self.pages:
            self.stack.addWidget(page)
        content_layout.addWidget(self.stack, 1)

        root_layout.addWidget(sidebar)
        root_layout.addWidget(content, 1)
        self.setCentralWidget(root)
        self.menu.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.menu.setCurrentRow(0)

    def dashboard_page(self) -> QWidget:
        page = Page("Genel Bakış", "Tamamı sentetik verilerle oluşturulmuş yönetim özeti")
        suppliers: list[Supplier] = self.data["suppliers"]  # type: ignore[assignment]
        customers: list[Customer] = self.data["customers"]  # type: ignore[assignment]
        accounts: list[CashAccount] = self.data["cash_accounts"]  # type: ignore[assignment]
        supplier_debt = sum((row.balance for row in suppliers), Decimal("0"))
        customer_receivable = sum((row.balance for row in customers), Decimal("0"))
        liquid = sum((row.balance for row in accounts), Decimal("0"))
        overdue = sum((row.overdue for row in suppliers), Decimal("0"))

        cards = QHBoxLayout()
        cards.setSpacing(14)
        cards.addWidget(MetricCard("Tedarikçi Borcu", money(supplier_debt), "5 sentetik cari", "#DC2626"))
        cards.addWidget(MetricCard("Müşteri Alacağı", money(customer_receivable), "5 sentetik cari", "#2563EB"))
        cards.addWidget(MetricCard("Likit Varlık", money(liquid), "4 demo hesap", "#059669"))
        cards.addWidget(MetricCard("Gecikmiş Tutar", money(overdue), "2 örnek kayıt", "#D97706"))
        page.layout.addLayout(cards)

        chart_box = QFrame()
        chart_box.setObjectName("panel")
        chart_layout = QVBoxLayout(chart_box)
        chart_title = QLabel("Aylık Satış Eğilimi")
        chart_title.setObjectName("panelTitle")
        chart_layout.addWidget(chart_title)
        chart_layout.addWidget(SalesChart(self.data["monthly_sales"]))  # type: ignore[arg-type]
        page.layout.addWidget(chart_box)
        return page

    def suppliers_page(self) -> QWidget:
        page = Page("Tedarikçiler", "Gerçek firma veya bakiye içermez")
        table = DataTable(["Cari Kod", "Tedarikçi", "Bakiye", "Gecikmiş", "Yaklaşan Vade"])
        rows = []
        for item in self.data["suppliers"]:  # type: ignore[union-attr]
            rows.append([item.code, item.name, money(item.balance), money(item.overdue), item.next_due.strftime("%d.%m.%Y")])
        table.set_rows(rows)
        page.layout.addWidget(table, 1)
        page.table = table  # type: ignore[attr-defined]
        return page

    def customers_page(self) -> QWidget:
        page = Page("Müşteriler", "Demo kredi limiti ve cari risk görünümü")
        table = DataTable(["Cari Kod", "Müşteri", "Bakiye", "Kredi Limiti", "Durum"])
        table.set_rows([[item.code, item.name, money(item.balance), money(item.credit_limit), item.status] for item in self.data["customers"]])  # type: ignore[union-attr]
        page.layout.addWidget(table, 1)
        page.table = table  # type: ignore[attr-defined]
        return page

    def transactions_page(self) -> QWidget:
        page = Page("Cari Hareketler", "Fatura, satış, tahsilat ve ödeme örnekleri")
        table = DataTable(["Belge", "Cari", "İşlem", "Tutar", "Tarih", "Vade", "Durum"])
        rows = []
        for item in self.data["transactions"]:  # type: ignore[union-attr]
            rows.append([item.document_no, item.party, item.kind, money(item.amount), item.transaction_date.strftime("%d.%m.%Y"), item.due_date.strftime("%d.%m.%Y") if item.due_date else "—", item.status])
        table.set_rows(rows)
        page.layout.addWidget(table, 1)
        page.table = table  # type: ignore[attr-defined]
        return page

    def finance_page(self) -> QWidget:
        page = Page("Kasa ve Banka", "Yerel olarak üretilmiş temsili hesap bakiyeleri")
        table = DataTable(["Hesap", "Tür", "Bakiye"])
        table.set_rows([[item.name, item.account_type, money(item.balance)] for item in self.data["cash_accounts"]])  # type: ignore[union-attr]
        page.layout.addWidget(table, 1)
        page.table = table  # type: ignore[attr-defined]
        return page

    def reports_page(self) -> QWidget:
        page = Page("Raporlar", "Public demo sürümünde dışa aktarma ve veri yükleme kapalıdır")
        for title, description in [
            ("Cari Yaşlandırma", "Gecikmiş ve yaklaşan örnek vadeleri gruplar."),
            ("Nakit Akışı", "Sentetik tahsilat ve ödeme hareketlerinden özet üretir."),
            ("Risk Analizi", "Demo kredi limiti ve bakiye ilişkisini gösterir."),
            ("Yönetim Özeti", "Temsili KPI ve aylık eğilimleri bir araya getirir."),
        ]:
            box = QFrame()
            box.setObjectName("reportCard")
            layout = QVBoxLayout(box)
            heading = QLabel(title)
            heading.setObjectName("panelTitle")
            detail = QLabel(description)
            detail.setObjectName("pageSubtitle")
            layout.addWidget(heading)
            layout.addWidget(detail)
            page.layout.addWidget(box)
        page.layout.addStretch(1)
        return page

    def filter_current_table(self, text: str) -> None:
        page = self.stack.currentWidget()
        table = getattr(page, "table", None)
        if not isinstance(table, QTableWidget):
            return
        query = text.strip().casefold()
        for row in range(table.rowCount()):
            visible = not query or any(query in (table.item(row, column).text().casefold() if table.item(row, column) else "") for column in range(table.columnCount()))
            table.setRowHidden(row, not visible)


STYLE = """
* { font-family: 'Segoe UI', 'Arial'; color: #172033; }
QMainWindow, #content { background: #F4F7FB; }
#sidebar { background: #111827; }
#logo { color: #FFFFFF; font-size: 28px; font-weight: 800; letter-spacing: 2px; }
#tagline { color: #94A3B8; font-size: 12px; }
#demoBadge { color: #BFDBFE; background: #1E3A8A; border-radius: 7px; padding: 7px 10px; font-weight: 700; }
#menu { background: transparent; border: 0; color: #CBD5E1; outline: 0; }
#menu::item { color: #CBD5E1; padding: 12px 13px; border-radius: 8px; }
#menu::item:selected { background: #2563EB; color: #FFFFFF; font-weight: 700; }
#menu::item:hover:!selected { background: #1F2937; }
#privacy { color: #93C5FD; background: #172554; border-radius: 9px; padding: 12px; line-height: 1.4; }
#topbar { background: #FFFFFF; border-bottom: 1px solid #E5E7EB; }
#state { color: #059669; font-weight: 700; }
QLineEdit { background: #F8FAFC; border: 1px solid #D7DEE9; border-radius: 8px; padding: 9px 12px; }
QPushButton { background: #E8EEF8; border: 0; border-radius: 8px; padding: 9px 16px; font-weight: 700; }
QPushButton:hover { background: #D8E3F4; }
#pageTitle { font-size: 26px; font-weight: 800; }
#pageSubtitle { color: #64748B; font-size: 13px; }
#metricCard, #panel, #reportCard { background: #FFFFFF; border: 1px solid #E4EAF2; border-radius: 12px; }
#metricTitle { color: #64748B; font-weight: 700; }
#metricValue { font-size: 24px; font-weight: 800; }
#metricNote { color: #94A3B8; }
#panelTitle { font-size: 16px; font-weight: 800; }
QTableWidget { background: #FFFFFF; border: 1px solid #E4EAF2; border-radius: 10px; alternate-background-color: #F8FAFC; selection-background-color: #DBEAFE; }
QHeaderView::section { background: #EEF3F9; border: 0; border-bottom: 1px solid #DCE4EF; padding: 11px; font-weight: 800; color: #475569; }
QTableWidget::item { padding: 10px; border-bottom: 1px solid #EEF2F7; }
"""


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName(APP_TITLE)
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(STYLE)
    window = Cari360Window()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
