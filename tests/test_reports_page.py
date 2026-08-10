import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from main import Cari360Window, DataTable


def test_reports_page_displays_all_aging_buckets():
    app = QApplication.instance() or QApplication([])
    window = Cari360Window()

    reports_page = window.stack.widget(5)
    table = getattr(reports_page, "table", None)

    assert isinstance(table, DataTable)
    assert table.rowCount() == 8
    assert table.columnCount() == 3
    assert table.horizontalHeaderItem(0).text() == "Vade Aralığı"
    assert table.item(0, 0).text() == "61+ gün gecikmiş"
    assert table.item(7, 0).text() == "31+ gün içinde"
    assert all(table.item(row, 2).text().startswith("₺") for row in range(table.rowCount()))

    window.close()
    app.processEvents()
