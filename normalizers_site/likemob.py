import re
from typing import Any


def fix_name_likemob(name: Any) -> str:
    """
    Applies specific string replacements to normalize the product name.
    Logic preserved from helpers.js returnFixNameLikemob
    """
    value = str(name or "")

    # Chain of replacements exactly as in the JS source
    value = value.replace("🚚", "")
    value = value.replace("Ноутбук ", "")
    value = value.replace("Gb", "")
    value = value.replace("NanoSIM ", "")
    value = value.replace("8+", "8/")
    value = value.replace("RU ", "")
    value = value.replace("3.75 ", "")
    value = value.replace("15+", "15 plus")
    value = value.replace("S24FE", "S24 FE")
    value = value.replace("S25FE", "S25 FE")
    value = value.replace("1T ", "1tb ")
    value = value.replace("Flip", "Z Flip")
    value = value.replace("Fold", "Z Fold")
    value = value.replace("14 Pro+", "14 pro +")
    value = value.replace("MI1", "Mi 1")
    value = value.replace("S10+", "s10 +")
    value = value.replace("LTE", "5G")
    value = value.replace("Watch7", "Watch 7")
    value = value.replace("SE(Gen 2)", "se2 ")
    value = value.replace("Watch 11", "S11")
    value = value.replace("Watch8", "Watch 8")
    value = value.replace("mm", "")
    value = value.replace("Navi", "Navy")
    value = value.replace("Nighfreeze", "Nightfreeze")
    value = value.replace("Lavander", "Lavender")
    value = value.replace("SE(Gen 3)", "SE3")
    
    return value.strip()


def return_name_in_arr_likemob(name: Any) -> str:
    """
    Extracts the clean product name for array matching.
    Logic preserved from helpers.js returnNameInArrLikemob
    """
    value = str(name or "")
    
    # Reverse the string
    reverse_str_name = value[::-1]
    
    # Fix Wi-Fi in reversed string (Wi-Fi -> iFiW)
    fix_wi_fi = reverse_str_name.replace("Wi-Fi", "WiFi")
    
    # Split by "-" and take the second part (index 1) if exists
    if "-" in fix_wi_fi:
        split_name = fix_wi_fi.split("-")[1]
    else:
        split_name = fix_wi_fi
        
    # Reverse back to original orientation
    reverse_back_str_name = split_name[::-1]
    
    # Fix Wi-Fi back (iFiW -> Wi-Fi)
    fix_wi_fi_final = reverse_back_str_name.replace("WiFi", "Wi-Fi")
    
    return fix_wi_fi_final.strip()


def return_stock_price_likemob(name: Any) -> str:
    """
    Extracts the price string from the raw input.
    Logic preserved from helpers.js returnStockPriceLikemob
    """
    value = str(name or "")
    to_lower_value = value.lower()
    
    # Reverse the string
    reverse_str_name = value[::-1]
    
    # Remove leading spaces (which are trailing in original)
    check_space1 = reverse_str_name[1:] if reverse_str_name and reverse_str_name[0] == " " else reverse_str_name
    check_space2 = check_space1[1:] if check_space1 and check_space1[0] == " " else check_space1
    check_space3 = check_space2[1:] if check_space2 and check_space2[0] == " " else check_space2
    check_space4 = check_space3[1:] if check_space3 and check_space3[0] == " " else check_space3
    
    # Fixes from to_lower_value before processing price extraction
    fix_wi_fi = to_lower_value.replace("wi-fi", "wifi")
    fix_usbc = fix_wi_fi.replace("usb-c", "usbc")
    fix_new = fix_usbc.replace("new", "")
    
    # If "-" exists, take the part after it (in the fixed/lowercase string)
    if "-" in fix_new:
        split_price = fix_new.split("-")[1]
    else:
        split_price = fix_new
        
    return split_price.strip()


def normalize_likemob_row(row: list[Any]) -> list[Any]:
    """
    Normalizes a single row from the Likemob supplier.
    """
    if not row:
        return []

    raw_value = str(row[0] or "").strip()

    if not raw_value:
        return []

    # Determine if we have a separate price column
    # Assuming standard format: [Name, Price] or [Raw_String]
    # Based on F51 logic: if len > 1 and row[1] exists, use separate logic
    if len(row) > 1 and row[1] not in ("", None):
        name = fix_name_likemob(raw_value)
        price = str(row[1]).strip()
    else:
        # If no separate price column, try to extract name and price from the single string
        name = return_name_in_arr_likemob(raw_value)
        price = return_stock_price_likemob(raw_value)

    # Basic validation: ensure price looks like a number and has reasonable length
    # F51 checks for digit length >= 5. We apply similar logic.
    digits_only = re.sub(r"\D", "", price)
    if len(digits_only) < 2: # Adjusted threshold, F51 used 5, but mobile prices can be smaller
        # If it looks empty or very short, return empty
        if not digits_only:
            return []

    return [name, price]