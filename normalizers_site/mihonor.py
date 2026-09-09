import re
from typing import Any


_PRICE_RE = re.compile(
    r"^(?P<name>.*?)\s+(?P<price>\d[\d\s.,]*)\s*₽\s*$"
)


def _split_name_price(value: str) -> tuple[str, str] | None:
    match = _PRICE_RE.match(value.strip())
    if not match:
        return None

    name = match.group("name").strip()
    price = match.group("price").strip()

    if not name or not price:
        return None

    return name, price


def _fix_flags(value: str) -> str:
    if len(value) < 2:
        return value

    return value[4:] + " " + value[:4]


def return_name_in_arr_mihonor(name: Any) -> str:
    value = str(name or "")
    parsed = _split_name_price(value)

    if parsed:
        return parsed[0]

    reversed_name = value[::-1]

    remove_space = (
        reversed_name[1:]
        if reversed_name and reversed_name[0] != "₽"
        else reversed_name
    )

    remove_rub = (
        remove_space[1:]
        if remove_space.startswith("₽")
        else reversed_name
    )

    split_price = (
        re.search(r"\s(.+)", remove_rub).group(1)
        if re.search(r"\s(.+)", remove_rub)
        else remove_rub
    )

    return _fix_flags(split_price[::-1])


def return_extra_price_mihonor(name: Any) -> Any:
    value = str(name or "")
    parsed = _split_name_price(value)

    if parsed:
        return parsed[1]

    reversed_name = value[::-1]

    remove_space = (
        reversed_name[1:]
        if reversed_name and reversed_name[0] != "₽"
        else reversed_name
    )

    remove_rub = (
        remove_space[1:]
        if remove_space.startswith("₽")
        else reversed_name
    )

    split_price = remove_rub.split(" ")[0] if " " in remove_rub else remove_rub
    price = split_price[::-1]

    return price


def return_stock_price_mihonor(name: Any) -> str:
    value = str(name or "")
    parsed = _split_name_price(value)

    if parsed:
        return parsed[1].replace("₽₽", "").replace("₽", "")

    if "₽ 2" in value:
        value = value.replace("₽ 2", "₽", 1)

    reversed_name = value[::-1]

    remove_space = (
        reversed_name[1:]
        if reversed_name and reversed_name[0] != "₽"
        else reversed_name
    )

    remove_rub = (
        remove_space[1:]
        if remove_space.startswith("₽")
        else reversed_name
    )

    split_price = remove_rub.split(" ")[0] if " " in remove_rub else remove_rub
    price = split_price[::-1]

    return price.replace("₽₽", "").replace("₽", "")


def fix_name_mihonor(name: Any) -> str:
    value = re.sub(r"\s+", " ", str(name or ""))

    replacements = [
        ("🆕", ""),
        ("GB", ""),
        ("Gb", ""),
        ("2+64", "2/64"),
        ("2+128", "2/128"),
        ("4+64", "4/64"),
        ("4+128", "4/128"),
        ("4+256", "4/256"),
        ("6+64", "6/64"),
        ("6+128", "6/128"),
        ("6+256", "6/256"),
        ("8+128", "8/128"),
        ("8+256", "8/256"),
        ("8+512", "8/512"),
        ("12+256", "12/256"),
        ("12+512", "12/512"),
        ("12+1TB", "12/1tb"),
        ("16+256", "16/256"),
        ("16+512", "16/512"),
        ("16+1TB", "15/1tb"),
        ("16+2TB", "16/2tb"),
        ("16+1024", "16/1tb"),
        ("A17 4G", "A17"),
        ("BLACК", "Black"),
        ("Z FLIP 7FE", "Z Flip 7 fe"),
        ("PRO PLUS", "Pro +"),
        ("8+256", "8/256"),
    ]

    for old, new in replacements:
        value = value.replace(old, "", 1) if new == "" else value.replace(old, new, 1)

    original_lower = str(name or "").lower()
    if return_name_in_arr_mihonor(original_lower).startswith("M"):
        value = value.replace("MI ", "XIAOMI ", 1)

    samsung_models = ("A25", "A26", "A35", "A36", "A55", "A56", "A57", "A37")
    if any(model in value for model in samsung_models):
        value = value.replace("5G ", "", 1)

    replacements = [
        ("8.7 4G ", ""),
        ("8.7 WI FI ", ""),
        ("LIGHT GREEN", "green"),
        ("SAMSUNG A9 PLUS", "Tab A9 +"),
        ("GREY", "gray"),
        ("LIGHT VIOLET", "violet"),
        ("+1024GB", "/1Tb"),
        ("8+255", "8/256"),
        ("8 256", "8/256"),
        ("8 128", "8/128"),
        ("12 256", "12/256"),
        ("6 128", "6/128"),
        ("4 128", "4/128"),
        ("12+1024", "12/1tb"),
        ("3+64", "3/64"),
        ("NOTE 14 PRO PLUS", "NOTE 14 PRO +"),
        ("12+ 512", "12/512"),
        ("LAVANDER", "Lavender"),
    ]

    for old, new in replacements:
        value = value.replace(old, new, 1)

    if "MI 13" in value or "MI 14" in value:
        value = value.replace("5G", "", 1)

    if "M55S" in value:
        value = value.replace("5G ", "", 1)

    if "X7" in value:
        value = value.replace("5G ", "", 1)

    return value


def normalize_mihonor_row(row: list[Any]) -> list[Any]:
    if not row:
        return []

    raw_text = str(row[0] or "").strip()
    if not raw_text:
        return []

    name = return_name_in_arr_mihonor(fix_name_mihonor(raw_text))

    price = (
        row[1]
        if len(row) > 1 and row[1] not in ("", None)
        else return_stock_price_mihonor(raw_text)
    )

    return [name, price]