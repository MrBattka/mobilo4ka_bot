import re
from typing import Any


def fix_name_unisale(name: Any) -> str:
    """
    Applies specific string replacements to normalize the product name.
    Logic preserved from helpers.js returnFixNameUniSale
    """
    value = str(name or "")

    # Memory units
    value = value.replace("Gb", "")
    value = value.replace("GB", "")

    # Colors
    value = value.replace("Space Black", "Black")
    value = value.replace("Space Gray", "Gray")
    value = value.replace("Lavander", "Lavender")

    # Fold/Flip Model Fixes
    value = value.replace("z fold6", "z fold 6")
    value = value.replace("z flip6", "z flip 6")
    value = value.replace("z fold7", "z fold 7")
    value = value.replace("z flip7", "z flip 7")
    value = value.replace("zflip", "z flip")

    # Accessories and Mouse
    value = value.replace("Magic Mouse (USB-C)", "Magic Mouse 3")
    value = value.replace("mm", "")

    # Wi-Fi and Connectivity
    value = value.replace("Wi‑Fi", "Wi-Fi") # Note: Non-breaking space in original might need normalization if present
    value = value.replace("Wi-Fi + LTE", "5G")

    # Apple Chips
    value = value.replace("(M4)", "M4")
    value = value.replace("(M3)", "M3")
    value = value.replace("(M5)", "M5")

    # Apple SE Models
    value = value.replace("SE (2024)", "SE2")
    value = value.replace("SE (2025)", "SE3")
    value = value.replace("SE 2 (2024)", "SE2")
    value = value.replace("SE 3 (2025)", "SE3")

    # Yandex and Disk
    value = value.replace("Yandex", "Яндекс")
    value = value.replace("Disk", "Disc")

    # Storage
    value = value.replace("/1024 ", "/1TB ")

    # Samsung Plus Models
    value = value.replace("s26 Plus", "S26+")
    value = value.replace("s25 Plus", "S25+")

    # SIM Types
    value = value.replace("E-Sim", "eSim")
    value = value.replace("Dual-Sim", "Dual")

    return value.strip()


def return_name_in_arr_unisale(name: Any) -> str:
    """
    Extracts the clean product name for array matching.
    Logic preserved from helpers.js returnNameInArrUniSale
    """
    value = str(name or "")
    
    # Reverse the string
    reverse_str_name = value[::-1]
    
    # Trim trailing spaces (leading in reverse)
    check_space1 = reverse_str_name[1:] if reverse_str_name and reverse_str_name[0] == " " else reverse_str_name
    check_space2 = check_space1[1:] if check_space1 and check_space1[0] == " " else check_space1
    check_space3 = check_space2[1:] if check_space2 and check_space2[0] == " " else check_space2
    check_space4 = check_space3[1:] if check_space3 and check_space3[0] == " " else check_space3
    
    # Split by hyphen. If hyphen exists, take the part after it.
    split_price = ""
    if "-" in check_space4:
        # Find first space and take everything after
        match = re.search(r"\s(.+)", check_space4)
        split_price = match.group(1) if match else check_space4
    else:
        split_price = check_space4
        
    # Reverse back
    reverse_back_str_name = split_price[::-1]
    
    return reverse_back_str_name.strip()


def return_stock_price_unisale(name: Any) -> str:
    """
    Extracts the price string from the raw input.
    Logic preserved from helpers.js returnStockPriceUniSale
    """
    value = str(name or "")
    
    # Reverse the string
    reverse_back_str_name = value[::-1]
    
    # Trim trailing spaces (leading in reverse)
    check_space1 = reverse_back_str_name[1:] if reverse_back_str_name and reverse_back_str_name[0] == " " else reverse_back_str_name
    check_space2 = check_space1[1:] if check_space1 and check_space1[0] == " " else check_space1
    check_space3 = check_space2[1:] if check_space2 and check_space2[0] == " " else check_space2
    check_space4 = check_space3[1:] if check_space3 and check_space3[0] == " " else check_space3
    
    # Split by space to get the first part (price)
    remove_other = check_space4.split(" ")[0] if " " in check_space4 else check_space4
    
    # Reverse again
    reverse_str_name = remove_other[::-1]
    
    # Remove backticks
    replace1 = reverse_str_name.replace("`", "")
    
    return replace1.strip()


def normalize_unisale_row(row: list[Any]) -> list[Any]:
    """
    Normalizes a single row from the UniSale supplier.
    """
    if not row:
        return []

    raw_value = str(row[0] or "").strip()

    if not raw_value:
        return []

    # Determine if we have a separate price column
    if len(row) > 1 and row[1] not in ("", None):
        name = fix_name_unisale(raw_value)
        price = str(row[1]).strip()
    else:
        # If no separate price column, try to extract name and price from the single string
        name = fix_name_unisale(return_name_in_arr_unisale(raw_value))
        price = return_stock_price_unisale(raw_value)

    # Basic validation: ensure price looks like a number
    digits_only = re.sub(r"\D", "", price)
    if len(digits_only) < 2:
        return []

    return [name, price]