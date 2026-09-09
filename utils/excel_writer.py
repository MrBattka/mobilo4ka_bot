import json
import os
from pathlib import Path
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Alignment, PatternFill
from config.settings import ALL_PRICE_FILE


def save_supplier_to_excel(
    chat_id: str,
    name: str,
    rows: list[list[str]],
    mode: str = "replace",
    sheet_number: int | None = None
):
    """Сохраняет данные поставщика в AllPrice.xlsx."""

    ALL_PRICE_FILE.parent.mkdir(parents=True, exist_ok=True)

    if ALL_PRICE_FILE.exists():
        try:
            wb = load_workbook(ALL_PRICE_FILE)
        except Exception:
            wb = Workbook()
    else:
        wb = Workbook()

    if not wb.worksheets:
        ws = wb.create_sheet(title="Лист 1")
    else:
        ws = wb.active

    if sheet_number is not None:
        sheet_index = max(1, int(sheet_number)) - 1

        while len(wb.worksheets) <= sheet_index:
            wb.create_sheet(title=f"Лист {len(wb.worksheets) + 1}")

        ws = wb.worksheets[sheet_index]
    elif name in wb.sheetnames:
        ws = wb[name]
    else:
        ws = wb.create_sheet(title=name)

    if mode == "replace":
        ws.delete_rows(1, ws.max_row)

    # Заголовки нужны только для Boltun и Trubkoved
    has_header = sheet_number in (25, 27, 28, 29)

    if has_header:
        ws["A1"] = "name"
        ws["B1"] = "price"

        for cell in ("A1", "B1"):
            ws[cell].font = Font(bold=True)
            ws[cell].alignment = Alignment(horizontal="center")

        start_row = 2
    else:
        start_row = 1 if mode == "replace" else max(1, ws.max_row + 1)

    for row_index, row in enumerate(rows, start=start_row):
        values = (
            [str(cell) if cell is not None else "" for cell in row]
            if isinstance(row, (list, tuple))
            else [str(row)]
        )

        for col_index, value in enumerate(values, start=1):
            ws.cell(
                row=row_index,
                column=col_index,
                value=value,
            )

    wb.save(ALL_PRICE_FILE)

    print(
        f"✅ Данные '{name}' сохранены в {ALL_PRICE_FILE} "
        f"(лист №{sheet_number or 1})"
    )