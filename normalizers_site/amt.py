import re
from typing import Any

FLAGS = [
    "🇯🇵", "🇮🇳", "🇪🇺", "🇦🇪", "🇧🇷", "🇻🇳", "🇰🇼", "🇺🇸",
    "🇭🇰", "🇬🇧", "🇨🇳", "🇹🇼", "🇷🇺", "🇦🇺", "🇨🇦", "🇨🇱",
    "🇹🇭", "🇸🇬", "🇲🇾", "🇨🇫", "🇰🇿", "🇰🇷", "🇬🇺", "🇿🇦", "🇵🇾"
]


def check_flags(str_val: str) -> str:
    """
    Moves trailing flag emojis to the beginning of the string.
    Logic preserved from JS checkFlags function.
    """
    
    str_stripped = str_val.rstrip()
    if not str_stripped:
        return str_val
        
    last_char = str_stripped[-1]
    
    if last_char in FLAGS:
        # Move the flag to the front
        flag = last_char
        return flag + str_stripped[:-1].lstrip() # lstrip to remove potential trailing space before flag
        
    return str_stripped


def fix_name_amt(name: Any) -> str:
    """
    Applies specific string replacements to normalize the product name.
    Logic preserved from helpers.js fixNameAMT
    """
    value = str(name or "")

    # Remove checkboxes and text
    value = value.replace("✅", "")
    value = value.replace("без СЗУ", "")
    value = value.replace("NFC", "")
    value = value.replace("+Чехол-клавиатура", "")
    value = value.replace("+ Чехол-клавиатура с тачпадом", "")

    # Model fixes
    value = value.replace("S9FE+", "S9 Fe +")
    value = value.replace("S9FE", "S9 FE")
    value = value.replace("4G ", "")
    value = value.replace("S10+", "S10 +")
    value = value.replace("A9+", "A9 +")
    value = value.replace("S25 Plus", "S25+")
    value = value.replace("S24 Plus", "S24+")
    value = value.replace("S24FE", "S24 FE")
    value = value.replace("S23FE", "S23 FE")
    value = value.replace("S22FE", "S22 FE")
    value = value.replace("S21FE", "S21 FE")
    value = value.replace("night freeze", "Nightfreeze")
    value = value.replace("S20FE", "S20 FE")
    value = value.replace("S23 Plus", "S23+")
    value = value.replace("S22 Plus", "S22+")
    value = value.replace("S21 Plus", "S21+")
    value = value.replace("S20 Plus", "S20+")
    value = value.replace("1 tb", "1tb")
    value = value.replace("1024", "1tb")
    value = value.replace("S10 FE Plus", "S10 FE +")
    value = value.replace("PocoPhone", "Poco")
    value = value.replace("PocoPad", "Poco Pad")
    value = value.replace("Note 14 Pro Plus", "Note 14 Pro +")
    value = value.replace("Redmi 14S", "Note 14S")
    value = value.replace("Watch (2025) 8", "Watch 8")
    value = value.replace("2 tb", "2TB")
    value = value.replace("Nothing Phone (3)", "Nothing Phone 3")
    value = value.replace("Grey", "Gray")
    value = value.replace("SE 2", "SE2")
    value = value.replace("SE 3", "SE3")
    value = value.replace("SE3 (2022)", "SE3")

    # Color translations
    value = value.replace("Черный", "Black")
    # Special case for Navy on Z Fold
    if "Z Fold" in value:
        value = value.replace(" Темно-Синий", "Navy")
    value = value.replace("Чёрный", "Black")
    value = value.replace("Зеленый", "Green")
    value = value.replace("Желтый", "Yellow")
    value = value.replace("Фиолетовый", "Purple")
    value = value.replace("Синий", "Blue")
    value = value.replace("Coral", "Red")
    value = value.replace("Серебро", "Silver")
    
    # Graphite logic
    if "S10 " in value or "S9 " in value:
        value = value.replace("Графит", "Gray")
    else:
        value = value.replace("Графит", "Graphite")
        
    value = value.replace("Бежевый", "Beige")
    value = value.replace("Лаванда", "Lavender")
    value = value.replace("Мятный", "Mint")
    value = value.replace("Мята", "Mint")
    value = value.replace("золото", "Gold")
    
    # Gray logic for Magic 7 Pro
    if "Magic 7 Pro" in value:
        value = value.replace("Серый", "White")
    else:
        value = value.replace("Серый", "Gray")
        
    value = value.replace("Голубой", "Blue")
    value = value.replace("Розовый", "Pink")
    value = value.replace("Белый", "")

    # Cyrillic 'A' to Latin 'A'
    if any(model in value for model in ["А16", "А25", "А26", "А35", "А36", "А55", "А56"]):
        value = value.replace("А", "A")

    # Remove 5G for specific models
    if any(model in value for model in ["A25", "A26", "A35", "A36", "A55", "A56", "A37", "A57"]):
        value = value.replace("5G ", "")
        
    # Pixel/Samsung/Redmi specific 5G removal
    if any(model in value for model in [
        "Pixel", "M55", "S21", "А36", "А56", "А25", "А26", "А35", "А54",
        "S22", "S23", "S24", "S25"
    ]):
        value = value.replace("5G ", "")

    # Remove 1sim
    value = value.replace("1sim", "")

    return value.strip()


def return_name_in_arr_amt(name: Any) -> str:
    """
    Extracts the clean product name for array matching.
    Logic preserved from helpers.js returnNameInArrAMT
    """
    value = str(name or "")
    
    # Check and move flags
    fix_flags = check_flags(value)
    
    # Reverse string
    reverse_str_name = fix_flags[::-1]
    
    # Trim trailing spaces (leading in reverse)
    check_space1 = reverse_str_name[1:] if reverse_str_name and reverse_str_name[0] == " " else reverse_str_name
    check_space2 = check_space1[1:] if check_space1 and check_space1[0] == " " else check_space1
    check_space3 = check_space2[1:] if check_space2 and check_space2[0] == " " else check_space2
    check_space4 = check_space3[1:] if check_space3 and check_space3[0] == " " else check_space3
    
    # Split by hyphen. If hyphen exists, take the part after it.
    # Note: JS uses regex `/\s(.+)/.exec(checkSpace4)[1]` which finds the first space and takes everything after.
    # However, the comment says `checkSpace4.indexOf("-") !== -1`.
    # Let's follow the JS logic: if "-" exists, use regex to find space? 
    # JS: `checkSpace4.indexOf("-") !== -1 ? /\s(.+)/.exec(checkSpace4)[1] : checkSpace4`
    # This implies: if there is a dash, split by space and take second part. If no dash, take whole string.
    
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


def return_stock_price_amt(name: Any) -> str:
    """
    Extracts the price string from the raw input.
    Logic preserved from helpers.js returnStockPriceAMT
    """
    value = str(name or "")
    
    # Remove all flags
    for flag in FLAGS:
        value = value.replace(flag, "")
        
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
    
    # Remove Silverblue and dots
    replace_silverblue = reverse_str_name.replace("Silverblue", "")
    replace_dot = replace_silverblue.replace(".", "")
    
    return replace_dot.strip()


def normalize_amt_row(row: list[Any]) -> list[Any]:
    """
    Normalizes a single row from the Trub/AMT supplier.
    """
    if not row:
        return []

    raw_value = str(row[0] or "").strip()

    if not raw_value:
        return []

    # Assuming raw value contains the full string
    # Apply name fixes
    name = fix_name_amt(return_name_in_arr_amt(raw_value))
    
    # Extract price
    price = return_stock_price_amt(raw_value)

    # Basic validation
    digits_only = re.sub(r"\D", "", price)
    if len(digits_only) < 2:
        return []

    return [name, price]