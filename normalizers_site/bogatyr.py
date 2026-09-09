import re
from typing import Any


def fix_name_a18(name: Any) -> str:
    """
    Applies specific string replacements to normalize the product name.
    Logic preserved from helpers.js returnFixNameA18
    """
    value = str(name or "")

    # Model name fixes
    value = value.replace("X7 ", "poco x7 ")
    value = value.replace("F7 ", "poco f7 ")
    value = value.replace("One Plus", "OnePlus")
    value = value.replace("Procelain", "porcelain")
    value = value.replace("S23FE", "S23 FE")
    value = value.replace("Steam Deck Black", "Steam Deck")
    value = value.replace("15+", "15 plus")
    value = value.replace("S24FE", "S24 FE")
    value = value.replace("1T ", "1tb ")
    value = value.replace("Flip", "Z Flip")
    value = value.replace("Fold", "Z Fold")
    value = value.replace("14 Pro+", "14 pro +")
    value = value.replace("MI1", "Mi 1")
    value = value.replace("S10+", "s10 +")
    value = value.replace("Rog ", "Rog Phone ")
    value = value.replace("LTE", "5G")
    value = value.replace("CE 4", "CE4")
    value = value.replace("Irbis", "iris")
    value = value.replace("S10 Plus", "S10 +")
    value = value.replace("Fros ", "Frost ")
    value = value.replace("S10FE Plus", "S10 FE +")
    value = value.replace("Lavander", "lavender")
    value = value.replace("Tab A11 Plus", "Tab A11 +")
    value = value.replace("Pro Plus", "Pro +")
    value = value.replace("2 TB", "2TB")

    # Conditional fixes
    if "X8 Pro" in value:
        value = value.replace("X8 Pro", "Poco X8 Pro")
    
    if "Pixel" in value:
        value = value.replace("White", "Snow")
        value = value.replace("Black", "Obsidian")

    return value.strip()


def return_name_in_arr_a18(name: Any) -> str:
    """
    Extracts the clean product name for array matching.
    Logic preserved from helpers.js returnNameInArrA18
    """
    value = str(name or "")
    
    # Reverse the string
    reverse_str_name = value[::-1]
    
    # Lowercase
    to_lower = reverse_str_name.lower()
    
    # Fix Wi-Fi in reversed string (wi-fi -> ifiw)
    fix_wi_fi = to_lower.replace("wi-fi", "wifi")
    
    # Split by "-" and take the second part (index 1) if exists
    if "-" in fix_wi_fi:
        split_name = fix_wi_fi.split("-")[1]
    else:
        split_name = fix_wi_fi
        
    # Reverse back to original orientation
    reverse_back_str_name = split_name[::-1]
    
    return reverse_back_str_name.strip()


def return_stock_price_a18(name: Any) -> str:
    """
    Extracts the price string from the raw input.
    Logic preserved from helpers.js returnStockPriceA18
    """
    value = str(name or "")
    to_lower_value = value.lower()
    
    # Reverse the string
    reverse_str_name = value[::-1]
    
    # Remove leading spaces (trailing in original)
    check_space1 = reverse_str_name[1:] if reverse_str_name and reverse_str_name[0] == " " else reverse_str_name
    check_space2 = check_space1[1:] if check_space1 and check_space1[0] == " " else check_space1
    check_space3 = check_space2[1:] if check_space2 and check_space2[0] == " " else check_space2
    check_space4 = check_space3[1:] if check_space3 and check_space3[0] == " " else check_space3
    
    # Fixes on the lowercase reversed string before processing
    fix_wi_fi = to_lower_value.replace("wi-fi", "wifi")
    fix_usbc = fix_wi_fi.replace("usb-c", "usbc")
    
    # Split by "-" to get potential price part
    if "-" in fix_usbc:
        split_price = fix_usbc.split("-")[1]
    else:
        split_price = fix_usbc
        
    # If no hyphen split occurred but there is a space, split by space
    if "-" not in split_price and " " in split_price:
        split_price = split_price.split(" ")[1]
        
    # Remove fire emojis
    split_fire = split_price.replace("🧨", "")
    split_double_fire = split_fire.replace("🧨", "")
    
    # Remove Ruble sign and dots
    replace_rub = split_double_fire.replace("₽", "")
    replace_dot = replace_rub.replace(".", "")
    
    return replace_dot.strip()


def normalize_bogatyr_row(row: list[Any]) -> list[Any]:
    """
    Normalizes a single row from the A18 supplier.
    """
    if not row:
        return []

    raw_value = str(row[0] or "").strip()

    if not raw_value:
        return []

    # Determine if we have a separate price column
    if len(row) > 1 and row[1] not in ("", None):
        name = fix_name_a18(raw_value)
        price = str(row[1]).strip()
    else:
        # If no separate price column, try to extract name and price from the single string
        name = fix_name_a18(return_name_in_arr_a18(raw_value))
        price = return_stock_price_a18(raw_value)

    # Basic validation: ensure price looks like a number
    digits_only = re.sub(r"\D", "", price)
    if len(digits_only) < 2:
        return []

    return [name, price]