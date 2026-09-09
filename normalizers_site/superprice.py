from typing import Any


def fix_name_super_price(name: Any) -> str:
    value = str(name or "")

    replacements = [
        ("S24 +", "S24+"),
        ("A25 5G", "A25"),
        ("A35 5G", "A35"),
        ("A54 5G", "A54"),
        ("A55 5G", "A55"),
        ("GB", ""),
        (" Gb", ""),
        ("Ice Blue", "Iceblue"),
        ("Sandstore", "Sandstone"),
        ("Grey", "Gray"),
        ("Z Fold6", "Z Fold 6"),
        ("Z Flip6", "Z Flip 6"),
        ("Z Fold5", "Z Fold 5"),
        ("Z Flip5", "Z Flip 5"),
        ("Watch5", "Watch 5"),
        ("Watch6", "Watch 6"),
        ("mm", ""),
        ("12 5G", "12"),
        ("12 Pro 5G", "12 Pro"),
        ("Lavander", "Lavender"),
        ("13 5G", "13"),
        ("13T 5G", "13T"),
        ("Z Flip7", "Z Flip 7"),
        ("Z Fold7", "Z Fold 7"),
        ("Z Flip8", "Z Flip 8"),
        ("Z Fold8", "Z Fold 8"),
        ("13T Pro 5G", "13T Pro"),
        ("14 5G", "14"),
        ("14 Ultra 5G", "14 Ultra"),
        ("A15 5G", "A15"),
        ("Scarlet", "Red"),
        ("1024", "1Tb"),
        ("Awesome ", ""),
        ("Platinum Silver 12/512", "12/512 Platinum Silver"),
        ("Phantom Black", "Black"),
        ("Tab A11 Plus", "Tab A11 +"),
        ("Midnight Black", "Black"),
        ("Watch8", "Watch 8"),
        ("Note 13 8/256 Iceblue", "Note 13 8/256 blue"),
        ("Tab S10+", "Tab S10 +"),
        ("Note 14 Pro+", "Note 14 Pro +"),
    ]

    for old, new in replacements:
        value = value.replace(old, new, 1)

    if "Xperia" in value:
        value = value.replace("5G ", "", 1)

    models = (
        "Pixel",
        "M55",
        "S21",
        "A26",
        "A36",
        "A56",
        "A37",
        "A57",
    )

    if any(model in value for model in models):
        value = value.replace("5G ", "", 1)

    if "Tab S" in value:
        value = value.replace("5G", "LTE", 1)

    return value

def normalize_superprice_row(row: list[Any]) -> list[Any]:
    if not row:
        return []

    name = fix_name_super_price(row[0])

    # Цена не изменяется и не проверяется
    price = row[1] if len(row) > 1 else ""

    return [name, price]