from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Путь к данным
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR_SITE = Path(__file__).parent.parent / "data/site_data"

# Выбираемые JSON-файлы
SELECTED_FILES = [
    "idProductAppleData.json",
    "idProductXiaomiData.json",
    "idProductSamsungData.json",
    "idProductGarminData.json",
    "idProductOtherBrandData.json",
    "idProductOtherBrandData2.json"
]

# Заголовки разделов (для 4-го листа)
SECTION_HEADERS = {
    'VALVE', 'SONY', 'GOOGLE', 'XBOX', 'NINTENDO', 'META', 'OCULUS', 'APPLE',
    'SAMSUNG', 'XIAOMI', 'PHILIPS', 'HUAWEI', 'Название', 'Цена'
}

BASE_DIR = Path(__file__).parent.parent

SUPPLIERS_FILE_ORDER = BASE_DIR / "suplires_order.json"
SUPPLIERS_FILE_SITE = BASE_DIR / "suplires_site.json"
ALL_PRICE_FILE = Path(__file__).parent.parent / "data" / "AllPrice.xlsx"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
CHANNEL_ID_TEST = os.getenv("CHANNEL_ID_TEST")
CHANNEL_ID_ORDER_PRICE = os.getenv("CHANNEL_ID_ORDER_PRICE")
SHEETS_ID_FOR_ORDER = os.getenv("SHEETS_ID_FOR_ORDER")
SHEETS_ID_REMAINS = os.getenv("SHEETS_ID_REMAINS")
SHEETS_ID_FOR_SITE = os.getenv("SHEETS_ID_FOR_SITE")
CREDENTIALS_FILE = os.getenv("CREDENTIALS_FILE")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE_1 = os.getenv("PHONE_1")