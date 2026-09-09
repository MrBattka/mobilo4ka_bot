import re
from typing import Any


def fix_name_root_opt(name: Any) -> str:
    """
    Applies specific string replacements to normalize the product name.
    Logic preserved from helpers.js returnFixNameRootOpt
    """
    value = str(name or "")

    # Remove product categories
    value = value.replace("Планшет ", "")
    value = value.replace("Смартфон ", "")
    value = value.replace("Портативная акустическая система ", "")
    value = value.replace("Наушники беспроводные ", "")
    value = value.replace("Наушники ", "")
    value = value.replace("Смарт-часы ", "")

    # Memory units and dimensions
    value = value.replace("Gb", "")
    value = value.replace("GB", "")
    value = value.replace("ГБ", "")
    value = value.replace("mm", "")
    value = value.replace("мм ", "")

    # Watch and Phone model fixes
    value = value.replace("Watch6", "Watch 6")
    value = value.replace("Watch7", "Watch 7")
    value = value.replace("S24FE", "s24 FE")
    value = value.replace("2а", "2a")
    value = value.replace("3а", "3a")
    value = value.replace("Z Flip7", "Z Flip 7")
    value = value.replace("Z Fold7", "Z Fold 7")
    value = value.replace("CE 5", "ce5")
    value = value.replace("S23FE", "s23 FE")
    value = value.replace("S25FE", "S25 FE")
    value = value.replace("Z Flip 7FE", "SZ Flip 7 FE")
    value = value.replace("Mi15", "Mi 15")
    value = value.replace("Magic7 Pro", "Magic 7 Pro")
    value = value.replace("Fold6", "Fold 6")
    value = value.replace("ProMax", "Pro Max")
    value = value.replace("Series 11", "S11")
    value = value.replace("Flip6", "Flip 6")
    value = value.replace("Series 10", "S10")

    # NFC and Bluetooth removal
    value = value.replace("NFC", "")
    value = value.replace("Беспроводные наушники ", "")

    # POCO/Galaxy specific 5G/EU removal
    if "POCO" in value or "Galaxy" in value:
        value = value.replace("5G ", "")
    if "POCO" in value:
        value = value.replace("EU", "")

    # CMF fix
    value = value.replace("CMF(Nothing)", "CMF")

    # Color translations
    value = value.replace("Синий", "Blue")
    value = value.replace("Красный", "Red")
    value = value.replace("Фиолетовый", "Purple")
    value = value.replace("Зеленый", "Green")
    value = value.replace("Черный", "Black")
    value = value.replace("Темно синий", "Black")
    value = value.replace("Серый", "Gray")
    value = value.replace("Желтый", "Yellow")
    value = value.replace("Бежевый", "Beige")
    value = value.replace("Оранжевый", "Orange")
    value = value.replace("Белый", "White")
    value = value.replace("Серебристый", "Silver")
    value = value.replace("Серебро", "Silver")
    value = value.replace("Фиолет", "Violet")
    value = value.replace("Мятный", "Mint")
    value = value.replace("Сирень", "Lilac")
    value = value.replace("Графит", "Graphite")
    value = value.replace("Золотой", "Gold")

    # Storage and Color nuances
    value = value.replace(" ТБ", "Tb")
    value = value.replace(",", "")
    value = value.replace("8/256, Gold", "8/256 Gold")
    value = value.replace("12/1T ", "12/1TB ")
    value = value.replace("16/1T ", "16/1TB ")
    value = value.replace("12/1 ", "12/1TB ")

    # Light Blue / Ice Blue nuances
    if "S25" in value:
        value = value.replace("Ice Blue", "icyblue")
    elif "A55 " in value:
        value = value.replace("Голубой", "Light Blue")
    else:
        value = value.replace("Голубой", "Iceblue")

    return value.strip()


def return_name_in_arr_root(name: Any) -> str:
    """
    Extracts the clean product name for array matching.
    Logic preserved from helpers.js returnNameInArrRoot
    """
    value = str(name or "")
    
    # Remove double spaces
    remove_double_space = re.sub(r"\s+", " ", value)
    
    # Replace hyphen with space
    stick_to_space = remove_double_space.replace("-", " ")
    
    # Reverse string
    reverse_str_name = stick_to_space[::-1]
    
    # Extract price portion if length > 7 and contains space
    split_price = ""
    if len(reverse_str_name) > 7 and " " in reverse_str_name:
        # Regex: space followed by rest of string
        match = re.search(r"\s(.+)", reverse_str_name)
        if match:
            split_price = match.group(1)
    else:
        split_price = remove_double_space

    # Reverse back to original orientation
    reverse_back_str_name = split_price[::-1]
    
    return reverse_back_str_name.strip()


def return_stock_price_root(name: Any) -> str:
    """
    Extracts the price string from the raw input.
    Logic preserved from helpers.js returnStockPriceRoot
    """
    value = str(name or "")
    
    # Reverse the string
    reverse_str_name = value[::-1]
    
    # Remove leading spaces (trailing in original)
    check_space1 = reverse_str_name[1:] if reverse_str_name and reverse_str_name[0] == " " else reverse_str_name
    check_space2 = check_space1[1:] if check_space1 and check_space1[0] == " " else check_space1
    check_space3 = check_space2[1:] if check_space2 and check_space2[0] == " " else check_space2
    check_space4 = check_space3[1:] if check_space3 and check_space3[0] == " " else check_space3
    
    # Reverse back to original orientation for further cleaning
    reverse_back_str_name = check_space4[::-1]
    
    # Apply fixes
    fix_wi_fi = reverse_back_str_name.replace("Wi-Fi", "WiFi")
    fix_usbc = fix_wi_fi.replace("usb-c", "usbc")
    fix_sm = fix_usbc.replace("SM-", "SM ")
    fix_new = fix_sm.replace("new", "")
    fix_wh1 = fix_new.replace("WH-1", "WH1")
    fix_stick1 = fix_wh1.replace(" — ", "-")
    fix_stick = fix_stick1.replace("- ", "-")
    
    # Split by "-" to get potential price part
    if "-" in fix_stick:
        split_price = fix_stick.split("-")[1]
    else:
        split_price = fix_stick
        
    # Extract the second part if there's a space
    if " " in split_price:
        match = re.search(r"\s(.+)", split_price)
        if match:
            split_price2 = match.group(1)
        else:
            split_price2 = split_price
    else:
        split_price2 = split_price
        
    return split_price2.strip()


def normalize_rootopt_row(row: list[Any]) -> list[Any]:
    """
    Normalizes a single row from the RootOpt supplier.
    """
    if not row:
        return []

    raw_value = str(row[0] or "").strip()

    if not raw_value:
        return []
    
    if len(row) > 1 and row[1] not in ("", None):
        name = fix_name_root_opt(raw_value)
        price = str(row[1]).strip()
    else:
        # Try to extract price from the raw value if not provided
        # Note: return_stock_price_root expects the raw name.
        price = return_stock_price_root(raw_value)
        name = fix_name_root_opt(return_name_in_arr_root(raw_value))

    # Basic validation for price
    digits_only = re.sub(r"\D", "", price)
    if len(digits_only) < 2:
        return []

    return [name, price]