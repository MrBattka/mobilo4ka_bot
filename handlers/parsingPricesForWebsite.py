from aiogram import Router, types
import json
from pathlib import Path
import config.settings as settings

from utils.telegram_loader import sync_suppliers_to_sheets, load_suppliers_config
from utils.external_parsers import run_parser_boltun, run_parser_trubkoved, run_parser_applegod, run_parser_store77
from utils.keyboards import get_main_menu_kb
from utils.excel_writer import save_supplier_to_excel
from utils.excel_with_id import export_all_price_with_id
from normalizers_site.applegod import normalize_applegod_rows
from normalizers_site.boltun import normalize_boltun_rows
from normalizers_site.trubkoved import normalize_trubkoved_rows
from normalizers_site.store77 import normalize_store77_rows


from config.settings import (
    SHEETS_ID_FOR_SITE,
    SUPPLIERS_FILE_SITE
)

router = Router()


def _save_supplier_to_allprice(name: str, rows, sheet_number: int):
    if not rows:
        return False

    save_supplier_to_excel(
        chat_id=name.lower(),
        name=name,
        rows=rows,
        mode="replace",
        sheet_number=sheet_number
    )
    return True


@router.message(lambda m: m.text in ["ВЫГРУЗКА ПОСТАВЩИКОВ"])
async def parsingPricesForWebsite(message: types.Message):
    btn = get_main_menu_kb()
    bot = message.bot

    await message.answer("⏳ Приступил к выгрузке поставщиков в локальный Excel...", parse_mode="Markdown", reply_markup=btn)
    await message.answer("📡 Загрузка данных Boltun: / Trubkoved / AppleGod / Store77 ...", parse_mode="Markdown")

    boltun_rows = await run_parser_boltun()
    boltun_rows = normalize_boltun_rows(boltun_rows)
    if _save_supplier_to_allprice("Boltun", boltun_rows, 25):
        await message.answer(f"✅ Boltun: {len(boltun_rows)} товаров добавлено", parse_mode="Markdown")
    else:
        await message.answer("⚠️ Boltun: не удалось загрузить данные", parse_mode="Markdown")

    trubkoved_rows = await run_parser_trubkoved(max_sections=2, delay=2.0)
    trubkoved_rows = normalize_trubkoved_rows(trubkoved_rows)
    
    if _save_supplier_to_allprice("Trubkoved", trubkoved_rows, 27):
        await message.answer(f"✅ Trubkoved: {len(trubkoved_rows)} товаров добавлено", parse_mode="Markdown")
    else:
        await message.answer("⚠️ Trubkoved: сервер недоступен или timeout", parse_mode="Markdown")
        
    applegod_rows = await run_parser_applegod()
    applegod_rows = normalize_applegod_rows(applegod_rows)

    if _save_supplier_to_allprice("AppleGod", applegod_rows, 28):
        await message.answer(
            f"✅ AppleGod: {len(applegod_rows)} товаров добавлено",
            parse_mode="Markdown",
        )
    else:
        await message.answer(
            "⚠️ AppleGod: не удалось загрузить данные",
            parse_mode="Markdown",
        )
        
    store77_rows = await run_parser_store77()
    store77_rows = normalize_store77_rows(store77_rows)
    
    if _save_supplier_to_allprice("Store77", store77_rows, 29):
        await message.answer(f"✅ Store77: {len(store77_rows)} товаров добавлено", parse_mode="Markdown")
    else:
        await message.answer("⚠️ Store77: не удалось загрузить данные", parse_mode="Markdown")

    suppliers_config = load_suppliers_config(SUPPLIERS_FILE_SITE)

    if suppliers_config:
        success = await sync_suppliers_to_sheets(
            suppliers_config,
            sheet_id=SHEETS_ID_FOR_SITE,
            suppliers_file=SUPPLIERS_FILE_SITE,
            use_excel_mode=True
        )

        if not success:
            await message.answer(
                "❌ Ошибка при обновлении данных.",
                parse_mode="Markdown",
            )
        else:
            await message.answer(
                "✅ Данные успешно сохранены в AllPrice.xlsx.",
                parse_mode="Markdown",
            )

        linked_count, total_count = export_all_price_with_id(
            suppliers_config,
        )

        await message.answer(
            f"✅ AllPriceWithID.xlsx создан.\n"
            f"Привязано: {linked_count} из {total_count}",
            parse_mode="Markdown",
        )

# ---- Встроенный редактор suppliers_site.json ----
def _admin_allowed(user_id: int) -> bool:
    admins = getattr(settings, "ADMIN_IDS", []) or getattr(settings, "ADMINS", [])
    if not admins:
        # если список админов не задан — разрешаем всем (можно изменить на жесткую блокировку)
        return True
    return user_id in admins

@router.message(lambda m: m.text and m.text.startswith("/get_suppliers"))
async def cmd_get_suppliers(message: types.Message):
    if not _admin_allowed(message.from_user.id):
        await message.answer("❌ Доступ запрещён.")
        return
    path = Path(SUPPLIERS_FILE_SITE)
    if not path.exists():
        await message.answer("❌ Файл конфигурации не найден.")
        return
    await message.answer_document(types.InputFile(path), caption="Текущая конфигурация поставщиков (suplires_site.json)")

@router.message(lambda m: m.document is not None)
async def on_document_receive(message: types.Message):
    """
    При получении JSON-файла — обновляем suplires_site.json.
    Документ должен быть JSON (расширение .json или mime application/json).
    """
    if not _admin_allowed(message.from_user.id):
        return
    doc = message.document
    fname = (doc.file_name or "").lower()
    if not (fname.endswith(".json") or (doc.mime_type and "json" in doc.mime_type)):
        return  # игнорируем другие файлы

    dest = Path(SUPPLIERS_FILE_SITE)
    await message.answer("⏳ Загружаю и проверяю файл...")
    try:
        await doc.download(destination_file=str(dest))
    except Exception as e:
        await message.answer(f"❌ Ошибка при загрузке файла: {e}")
        return

    try:
        with dest.open("r", encoding="utf-8") as f:
            loaded = json.load(f)
        # простая валидация — должен быть dict
        if not isinstance(loaded, dict):
            raise ValueError("Корневой объект должен быть JSON-объектом (dict).")
    except Exception as e:
        await message.answer(f"❌ Неверный JSON: {e}")
        return

    await message.answer("✅ Конфигурация успешно обновлена.")

@router.message(lambda m: m.text and m.text.startswith("/update_suppliers"))
async def cmd_update_suppliers_text(message: types.Message):
    """
    Обновление конфигурации передачей JSON в тексте сообщения:
    /update_suppliers {"@id": {...}, ...}
    """
    if not _admin_allowed(message.from_user.id):
        await message.answer("❌ Доступ запрещён.")
        return
    payload = message.text.partition(" ")[2].strip()
    if not payload:
        await message.answer("ℹ️ Подайте JSON после команды или загрузите файл .json")
        return
    try:
        parsed = json.loads(payload)
        if not isinstance(parsed, dict):
            raise ValueError("Ожидается JSON-объект.")
    except Exception as e:
        await message.answer(f"❌ Ошибка парсинга JSON: {e}")
        return
    dest = Path(SUPPLIERS_FILE_SITE)
    try:
        with dest.open("w", encoding="utf-8") as f:
            json.dump(parsed, f, ensure_ascii=False, indent=2)
    except Exception as e:
        await message.answer(f"❌ Не удалось сохранить файл: {e}")
        return
    await message.answer("✅ Конфигурация успешно обновлена (из текста).")

    # Уведомление админу (если нужно)
    try:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f"✅ Выгрузка завершена. Файл: <code>AllPrice.xlsx</code>",
            parse_mode="Markdown"
        )
    except:
        pass