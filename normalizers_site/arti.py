import re
from typing import Any


def fix_name_arti(name: Any) -> str:
    value = str(name or "")

    replacements = [
        ("📱*", " "),
        ("📱", ""),
        ("🆕*", " "),
        ("💻*", " "),
        ("🖥*", " "),
        ("📋*", " "),
        ("⭐", " "),
        ("2(USB-C)", "2 USB-C"),
        ("(USB-C)", "USB-C"),
        ("4(шумодав)", "4 anc"),
        ("(2023)", "2023"),
        ("🔥", ""),
        ("6⃣", "6"),
        ("*", ""),
        ("🎧", ""),
        ("✏️", ""),
        ("📋", ""),
        ("1⃣", "1"),
        ("2⃣", "2"),
        ("3⃣", "3"),
        ("(2Sim)", ""),
        ("(+клавиатура)", ""),
        ("S24 Plus", "S24+"),
        ("S23 Plus", "S23+"),
        ("S9 Fe Plus", "S9 FE +"),
        ("2️⃣0️⃣2️⃣4️⃣", " 2024"),
        ("8/255", "8/256"),
        ("4⃣", "4"),
        ("(", ""),
        (")", ""),
        (" S711B", ""),
        (" S918B", ""),
        (" S9160", ""),
        (" S911B", ""),
        (" S9210", ""),
        (" S921B", ""),
        (" S9280", ""),
        (" S928B", ""),
        (" S926B", ""),
        (" F731B", ""),
        (" F946B", ""),
        (" AI2401", ""),
        (" AI2302", ""),
        (" X710", ""),
        (" X810", ""),
        (" XQ-EC72", ""),
        (" 5G XQ-ES72", ""),
        (" XQ-DQ72", ""),
        ("NX721J ", ""),
        ("NE2213 ", ""),
        ("CPH2609 ", ""),
        ("CPH2493 ", ""),
        ("NX769J ", ""),
        ("XQ-DE72 ", ""),
        ("S916B ", ""),
        ("F956B ", ""),
        ("S721B ", ""),
        ("F741B ", ""),
        ("AirPods Pro2", "AirPods Pro 2"),
        ("AirPods Pro3", "AirPods Pro 3"),
        ("Z Fold7⃣", "Z Fold 7"),
        ("❄", "Icyblue"),
        ("iPad Pro1️⃣", "iPad Pro 1"),
        ("16P ", "16 Pro "),
        ("16PM ", "16 Pro Max "),
        ("AirPods4", "AirPods 4"),
        ("5️⃣", " 5 "),
        ("6️⃣", " 6 "),
        ("AirPods3", "AirPods 3"),
        ("Flip7⃣", "Flip 7"),
        ("💕", " Pink"),
        ("🔘", " Gray"),
        ("🟠", " Orange"),
        ("🟡", " Yellow"),
        ("🔴", " Red"),
        ("Crafted Black", "Black"),
        ("17P 256", "17 Pro 256"),
        ("17P 512", "17 Pro 512"),
        ("17P 1TB", "17 Pro 1TB"),
        ("17PM 256", "17 Pro Max 256"),
        ("17PM 512", "17 Pro Max 512"),
        ("17PM 1TB", "17 Pro Max 1TB"),
        ("17PM 2TB", "17 Pro Max 2TB"),
    ]

    # Особая обработка цветов
    if "iPad" in value and "iPad Pro" not in value:
        value = value.replace("⚫", " Gray", 1)
    elif "14 " in value or "13 " in value:
        value = value.replace("⚫", " Midnight", 1)
    else:
        value = value.replace("⚫", " Black", 1)

    if "S24" in value or "S23" in value:
        value = value.replace("🟣", " Violet", 1)
    else:
        value = value.replace("🟣", " Purple", 1)

    if "iPad" in value:
        value = value.replace("⚪", " Silver", 1)
    else:
        value = value.replace("⚪", " White", 1)

    if any(f"16 {memory}" in value for memory in ("128", "256", "512")):
        value = value.replace("🔵", " Ultramarine", 1)
    else:
        value = value.replace("🔵", " Blue", 1)

    if "16 Pro" in value or any(
        f"16 {memory}" in value for memory in ("128", "256", "512")
    ):
        value = value.replace("🟢", " Teal", 1)
    else:
        value = value.replace("🟢", " Green", 1)

    if "S9 F" in value:
        value = value.replace("Black", "Gray", 1)

    if "S9 " in value:
        value = value.replace("Black", "Graphite", 1)
        value = value.replace("Purple", "Lavender", 1)
        value = value.replace("White", "Beige", 1)

    if "Z Flip 6 " in value:
        value = value.replace("Green", "Mint", 1)

    if "Z Flip 6 " in value or "Z Fold 6 " in value:
        value = value.replace("Gray", "Silver", 1)

    if "Z Fold 6 " in value:
        value = value.replace("Blue", "Navy", 1)

    for old, new in replacements:
        value = value.replace(old, new, 1)

    if "AirPods" in value:
        value = value.replace("🔇", " ANC", 1)

    if "S25 " in value and "Ultra" not in value:
        value = value.replace("Gray", "Silver", 1)

    return re.sub(r"\s+", " ", value).strip()


def return_name_arti(name: Any) -> str:
    value = str(name or "")[::-1]
    parts = value.split("-")

    if len(parts) >= 5:
        value = "-".join(parts[1:5])

    parts = value.split("-")
    if len(parts) >= 4:
        value = "-".join(parts[1:4])

    parts = value.split("-")
    if len(parts) >= 3:
        value = "-".join(parts[1:3])

    return value[::-1]


def return_stock_price_arti(name: Any) -> str:
    value = str(name or "")[::-1]

    if "-" in value:
        price = value.split("-")[0]
    else:
        price = value.split(" ")[0]

    price = price.replace(" ", "")[::-1]
    return price.replace("Блок❌", "")


def return_extra_price_arti(name: Any) -> Any:
    product_name = fix_name_arti(return_name_arti(name))
    price = return_stock_price_arti(name)

    return price


def normalize_arti_row(row: list[Any]) -> list[Any]:
    if not row:
        return []

    raw_value = str(row[0] or "").strip()
    if not raw_value:
        return []

    if len(row) > 1 and row[1] not in ("", None):
        name = fix_name_arti(raw_value)
        price = str(row[1]).strip()
    else:
        name = fix_name_arti(return_name_arti(raw_value))
        price = return_stock_price_arti(raw_value)

    if len(re.sub(r"\D", "", price)) < 5:
        return []

    return [name, price]