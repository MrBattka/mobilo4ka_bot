import asyncio
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk, simpledialog, filedialog
from aiogram import Bot
import sys
import json
import os
from pathlib import Path
import subprocess
import traceback

from config.settings import BOT_TOKEN, SUPPLIERS_FILE_SITE
from handlers.base import send_stock_price as send_stock_handler
from handlers.order import send_order_price as send_order_handler
from handlers.refreshPrice import refresh_stock_price as refresh_price_handler
from handlers.remains import send_stock_price as update_remains_handler
from handlers.parsingPricesForWebsite import parsingPricesForWebsite as update_upload_orders

if sys.platform == "win32" and sys.version_info >= (3, 8):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# === Эмуляция message для aiogram ===
class FakeMessage:
    def __init__(self, bot, text, from_user_id=123456789):
        self.bot = bot
        self.text = text
        self.from_user = type('User', (), {'id': from_user_id})()
        self.chat = self.from_user

    async def answer(self, text, reply_markup=None, parse_mode=None):
        append_log(f"{text}\n")


# === Глобальные переменные ===
bot = Bot(token=BOT_TOKEN) if BOT_TOKEN else None
is_running = False  # Флаг выполнения задачи

# === Логирование в текстовое поле ===
def append_log(text):
    def add():
        log_area.configure(state='normal')
        log_area.insert(tk.END, text)
        log_area.see(tk.END)
        log_area.configure(state='disabled')

    try:
        root.after(0, add)
    except Exception:
        # если GUI ещё не создан — игнор
        print(text)


# === Утилиты для конфигурации поставщиков ===
SUPPLIERS_PATH = Path(SUPPLIERS_FILE_SITE) if SUPPLIERS_FILE_SITE else Path.cwd() / "suplires_site.json"

def load_suppliers():
    try:
        if not SUPPLIERS_PATH.exists():
            SUPPLIERS_PATH.write_text("{}", encoding="utf-8")
        with SUPPLIERS_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("Корневой объект должен быть dict")
            return data
    except Exception as e:
        append_log(f"[Ошибка] Не удалось загрузить конфиг: {e}\n")
        return {}

def save_suppliers(data: dict):
    try:
        SUPPLIERS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        append_log("✅ Конфигура сохранена на диск.\n")
        return True
    except Exception as e:
        append_log(f"[Ошибка] Не удалось сохранить конфиг: {e}\n")
        return False

# === Продвинутый редактор конфигурации (список + форма) ===
def show_config_editor():
        try:
            cfg = load_suppliers()
            editor = tk.Toplevel(root)
            editor.title("Редактор suplires_site.json — Mobilo4ka")
            editor.geometry("1000x600")

            # левый список ключей
            left_frame = tk.Frame(editor, width=300)
            left_frame.pack(side="left", fill="y", padx=8, pady=8)
            tk.Label(left_frame, text="Поставщики:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
            lb = tk.Listbox(left_frame, width=40, exportselection=False)
            lb.pack(fill="y", expand=True, pady=(4,6))

            # кнопки для списка
            list_btns = tk.Frame(left_frame)
            list_btns.pack(fill="x", pady=(0,6))
            def add_supplier():
                key = simpledialog.askstring("Новый поставщик", "Введите chat_id или @username (ключ):", parent=editor)
                if not key:
                    return
                key = key.strip()
                if key in cfg:
                    messagebox.showwarning("Внимание", "Ключ уже существует")
                    return
                cfg[key] = {
                    "name": "",
                    "title": "",
                    "skip": False,
                    "numberList": 1,
                    "readExcel": False,
                    "excelColumns": {},
                    "todayMessage": False,
                    "replaceOld": False
                }
                refresh_list()
                lb.selection_clear(0, tk.END)
                idx = list(cfg.keys()).index(key)
                lb.selection_set(idx)
                on_select(None)

            def remove_supplier():
                sel = lb.curselection()
                if not sel:
                    return
                key = lb.get(sel[0])
                if not messagebox.askyesno("Удалить", f"Удалить поставщика {key}?"):
                    return
                cfg.pop(key, None)
                refresh_list()
                clear_form()

            ttk.Button(list_btns, text="Добавить", command=add_supplier, width=12).pack(side="left", padx=4)
            ttk.Button(list_btns, text="Удалить", command=remove_supplier, width=12).pack(side="left", padx=4)
            ttk.Button(list_btns, text="Открыть файл", command=open_config_in_editor, width=12).pack(side="left", padx=4)

            # правая панель — форма с прокруткой
            right_frame = tk.Frame(editor)
            right_frame.pack(side="right", fill="both", expand=True, padx=8, pady=8)

            form_canvas = tk.Canvas(right_frame)
            form_scroll = ttk.Scrollbar(right_frame, orient="vertical", command=form_canvas.yview)
            form_inner = tk.Frame(form_canvas)
            form_inner.bind("<Configure>", lambda e: form_canvas.configure(scrollregion=form_canvas.bbox("all")))
            form_canvas.create_window((0,0), window=form_inner, anchor="nw")
            form_canvas.configure(yscrollcommand=form_scroll.set)
            form_canvas.pack(side="left", fill="both", expand=True)
            form_scroll.pack(side="right", fill="y")

            # grid настройка
            form_inner.grid_columnconfigure(0, minsize=180)
            form_inner.grid_columnconfigure(1, weight=1)

            # поля формы (в виде grid, ровные строки)
            entries = {}
            bool_vars = {}
            row_idx = 0

            def add_label(col_text, r):
                lbl = tk.Label(form_inner, text=col_text, anchor="w")
                lbl.grid(row=r, column=0, sticky="w", padx=(6,10), pady=6)
                return lbl

            def add_widget(widget, r, colspan=1):
                widget.grid(row=r, column=1, columnspan=colspan, sticky="ew", padx=(0,6), pady=6)
                return widget

            # name
            add_label("name:", row_idx)
            entries['name'] = add_widget(tk.Entry(form_inner), row_idx); row_idx += 1
            
            add_label("title (one per line):", row_idx)
            entries['title'] = add_widget(scrolledtext.ScrolledText(form_inner, height=3), row_idx); row_idx += 1

            # skip (checkbox)
            add_label("skip:", row_idx)
            bool_vars['skip'] = tk.BooleanVar()
            entries['skip_chk'] = add_widget(tk.Checkbutton(form_inner, variable=bool_vars['skip']), row_idx)
            row_idx += 1

            # numberList
            add_label("numberList:", row_idx)
            entries['numberList'] = add_widget(tk.Spinbox(form_inner, from_=0, to=9999), row_idx); row_idx += 1

            # readExcel
            add_label("readExcel:", row_idx)
            bool_vars['readExcel'] = tk.BooleanVar()
            entries['readExcel_chk'] = add_widget(tk.Checkbutton(form_inner, variable=bool_vars['readExcel']), row_idx)
            row_idx += 1

            # excelColumns.price
            add_label("excelColumns.price:", row_idx)
            entries['excel_price'] = add_widget(tk.Entry(form_inner), row_idx); row_idx += 1

            # todayMessage
            add_label("todayMessage:", row_idx)
            bool_vars['todayMessage'] = tk.BooleanVar()
            entries['todayMessage_chk'] = add_widget(tk.Checkbutton(form_inner, variable=bool_vars['todayMessage']), row_idx)
            row_idx += 1

            # replaceOld
            add_label("replaceOld:", row_idx)
            bool_vars['replaceOld'] = tk.BooleanVar()
            entries['replaceOld_chk'] = add_widget(tk.Checkbutton(form_inner, variable=bool_vars['replaceOld']), row_idx)
            row_idx += 1

            # txtMessageHandle
            add_label("txtMessageHandle:", row_idx)
            entries['txtMessageHandle'] = add_widget(tk.Entry(form_inner), row_idx); row_idx += 1

            # numMessages
            add_label("numMessages:", row_idx)
            entries['numMessages'] = add_widget(tk.Spinbox(form_inner, from_=0, to=100), row_idx); row_idx += 1

            # messageIds (multiline)
            add_label("messageIds (one per line):", row_idx)
            entries['messageIds'] = add_widget(scrolledtext.ScrolledText(form_inner, height=4), row_idx); row_idx += 1

            # messageCodeWord
            add_label("messageCodeWord (one per line):", row_idx)
            entries['messageCodeWord'] = add_widget(scrolledtext.ScrolledText(form_inner, height=3), row_idx); row_idx += 1

            # banCodeWord
            add_label("banCodeWord (one per line):", row_idx)
            entries['banCodeWord'] = add_widget(scrolledtext.ScrolledText(form_inner, height=3), row_idx); row_idx += 1

            # Сброс/сохранить текущую запись
            def clear_form():
                for k, w in entries.items():
                    if isinstance(w, (tk.Entry, tk.Spinbox)):
                        try:
                            w.delete(0, tk.END)
                        except Exception:
                            pass
                    elif isinstance(w, scrolledtext.ScrolledText):
                        w.delete("1.0", tk.END)
                for v in bool_vars.values():
                    v.set(False)

            def populate_form(key, data):
                # helper moved above usage
                def fill_textfield(field_name, lst):
                    w = entries[field_name]; w.delete("1.0", tk.END)
                    if isinstance(lst, list):
                        w.insert("1.0", "\n".join(str(x) for x in lst))
                    elif isinstance(lst, str) and lst:
                        w.insert("1.0", lst)

                entries['name'].delete(0, tk.END); entries['name'].insert(0, data.get("name",""))
                fill_textfield('title', data.get("title", []))
                bool_vars['skip'].set(bool(data.get("skip", False)))
                entries['numberList'].delete(0, tk.END); entries['numberList'].insert(0, str(data.get("numberList", "")))
                bool_vars['readExcel'].set(bool(data.get("readExcel", False)))
                entries['excel_price'].delete(0, tk.END)
                excel = data.get("excelColumns", {})
                if isinstance(excel, dict):
                    entries['excel_price'].insert(0, str(excel.get("price","")))
                bool_vars['todayMessage'].set(bool(data.get("todayMessage", False)))
                bool_vars['replaceOld'].set(bool(data.get("replaceOld", False)))
                entries['txtMessageHandle'].delete(0, tk.END); entries['txtMessageHandle'].insert(0, data.get("txtMessageHandle",""))
                entries['numMessages'].delete(0, tk.END); entries['numMessages'].insert(0, str(data.get("numMessages","")))
                fill_textfield('messageIds', data.get("messageIds", []))
                fill_textfield('messageCodeWord', data.get("messageCodeWord", []))
                fill_textfield('banCodeWord', data.get("banCodeWord", []))

            def write_form_to_data(key):
                if key not in cfg:
                    return
                d = cfg[key]
                d["name"] = entries['name'].get().strip()
                d["title"] = read_list("title")
                d["skip"] = bool(bool_vars['skip'].get())
                try:
                    d["numberList"] = int(entries['numberList'].get())
                except Exception:
                    d["numberList"] = entries['numberList'].get()
                d["readExcel"] = bool(bool_vars['readExcel'].get())
                ex_price = entries['excel_price'].get().strip()
                if ex_price == "":
                    d["excelColumns"] = d.get("excelColumns", {})
                    d["excelColumns"].pop("price", None)
                else:
                    try:
                        d["excelColumns"] = d.get("excelColumns", {})
                        d["excelColumns"]["price"] = int(ex_price)
                    except Exception:
                        d["excelColumns"] = d.get("excelColumns", {})
                        d["excelColumns"]["price"] = ex_price
                d["todayMessage"] = bool(bool_vars['todayMessage'].get())
                d["replaceOld"] = bool(bool_vars['replaceOld'].get())
                d["txtMessageHandle"] = entries['txtMessageHandle'].get().strip()
                try:
                    d["numMessages"] = int(entries['numMessages'].get())
                except Exception:
                    d["numMessages"] = entries['numMessages'].get()
                def read_list(field):
                    txt = entries[field].get("1.0", "end").strip()
                    if not txt:
                        return []
                    return [x.strip() for x in txt.splitlines() if x.strip()]
                d["messageIds"] = read_list("messageIds")
                d["messageCodeWord"] = read_list("messageCodeWord")
                d["banCodeWord"] = read_list("banCodeWord")
                cfg[key] = d
                append_log(f"💾 Сохранено в памяти: {key}\n")

            def on_select(event):
                sel = lb.curselection()
                if not sel:
                    clear_form()
                    return
                key = lb.get(sel[0])
                data = cfg.get(key, {})
                populate_form(key, data)

            def save_current():
                sel = lb.curselection()
                if not sel:
                    messagebox.showinfo("Инфо", "Выберите поставщика слева")
                    return
                key = lb.get(sel[0])
                write_form_to_data(key)
                refresh_list()
                save_suppliers(cfg)

            def save_all_and_close():
                sel = lb.curselection()
                if sel:
                    write_form_to_data(lb.get(sel[0]))
                if save_suppliers(cfg):
                    editor.destroy()

            def export_json():
                path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files","*.json")])
                if not path:
                    return
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(cfg, f, ensure_ascii=False, indent=2)
                append_log(f"📤 Экспорт конфигурации в {path}\n")

            def refresh_list():
                lb.delete(0, tk.END)
                for k in cfg.keys():
                    lb.insert(tk.END, k)

            # нижняя панель кнопок
            btn_frame = tk.Frame(form_inner)
            btn_frame.grid(row=row_idx, column=0, columnspan=2, sticky="ew", pady=(12,4))
            ttk.Button(btn_frame, text="Сохранить текущую", command=save_current).pack(side="right", padx=4)
            ttk.Button(btn_frame, text="Сохранить все и закрыть", command=save_all_and_close).pack(side="right", padx=4)
            ttk.Button(btn_frame, text="Экспорт...", command=export_json).pack(side="right", padx=4)
            ttk.Button(btn_frame, text="Перезагрузить с диска", command=lambda: (lambda: (nonlocal_reload()))()).pack(side="left", padx=4)

            def nonlocal_reload():
                nonlocal cfg
                cfg = load_suppliers()
                refresh_list()
                clear_form()
                append_log("🔁 Конфиг перезагружен с диска.\n")

            # Инициализация списка и выбор первого
            refresh_list()
            if lb.size() > 0:
                lb.selection_set(0)
                on_select(None)

            lb.bind("<<ListboxSelect>>", on_select)
            editor.transient(root)
            editor.grab_set()
        except Exception:
            append_log(f"[Ошибка] Не удалось открыть редактор конфигурации:\n{traceback.format_exc()}\n")


def open_config_in_editor():
    try:
        if not SUPPLIERS_PATH.exists():
            SUPPLIERS_PATH.write_text("{}", encoding="utf-8")
        # Windows: notepad; cross-platform uses default app
        if sys.platform == "win32":
            os.startfile(str(SUPPLIERS_PATH))
        else:
            subprocess.Popen(["xdg-open" if sys.platform.startswith("linux") else "open", str(SUPPLIERS_PATH)])
        append_log(f"📁 Открыт файл конфигурации: {SUPPLIERS_PATH}\n")
    except Exception as e:
        append_log(f"[Ошибка] Не удалось открыть файл: {e}\n")


# === Асинхронные задачи ===
async def run_send_stock_price(mode):
    msg = "ПРАЙС ПО НАЛИЧИЮ" if mode == "main" else "ПРАЙС ПО НАЛИЧИЮ (тест)"
    fake_message = FakeMessage(bot, msg)
    await send_stock_handler(fake_message)


async def run_send_order_price(mode):
    from aiogram import Bot
    from config.settings import BOT_TOKEN

    local_bot = Bot(token=BOT_TOKEN) if BOT_TOKEN else None
    msg = "ПРАЙС ПОД ЗАКАЗ" if mode == "main" else "ПРАЙС ПОД ЗАКАЗ (тест)"
    fake_message = FakeMessage(local_bot, msg)
    try:
        await send_order_handler(fake_message)
    finally:
        if local_bot:
            try:
                await local_bot.session.close()
            except Exception:
                pass


async def run_refresh_stock_price():
    fake_message = FakeMessage(bot, "ОБНОВИТЬ ЦЕНЫ ОПТ")
    await refresh_price_handler(fake_message)


async def run_update_remains():
    fake_message = FakeMessage(bot, "ПРОСТАВИТЬ ЦЕНЫ В ОСТАТКАХ")
    await update_remains_handler(fake_message)
    
async def run_upload_orders():
    fake_message = FakeMessage(bot, "ВЫГРУЗКА ПОСТАВЩИКОВ")
    await update_upload_orders(fake_message)


# === Запуск асинхронной задачи в отдельном потоке ===
def run_async_task(coro):
    def task():
        global is_running
        is_running = True
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            if sys.platform == "win32":
                loop.set_debug(False)
                try:
                    from asyncio import WindowsSelectorEventLoopPolicy
                    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
                except Exception:
                    pass
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            loop.run_until_complete(coro)
        except Exception as e:
            append_log(f"[Ошибка] {e}\n")
            append_log(traceback.format_exc() + "\n")
        finally:
            try:
                loop.close()
            except Exception:
                pass
            try:
                asyncio.set_event_loop(None)
            except Exception:
                pass
            is_running = False
            try:
                root.after(0, enable_buttons)
            except Exception:
                pass

    threading.Thread(target=task, daemon=True).start()


# === Обёртки для запуска ===
def start_send_stock_main():
    if not is_running:
        disable_buttons()
        append_log("🔄 Запуск: ПРАЙС ПО НАЛИЧИЮ (основной)\n")
        run_async_task(run_send_stock_price("main"))
    else:
        messagebox.showwarning("Подождите", "Уже выполняется задача!")


def start_send_stock_test():
    if not is_running:
        disable_buttons()
        append_log("🔄 Запуск: ПРАЙС ПО НАЛИЧИЮ (тест)\n")
        run_async_task(run_send_stock_price("test"))
    else:
        messagebox.showwarning("Подождите", "Уже выполняется задача!")


def start_send_order_main():
    if not is_running:
        disable_buttons()
        append_log("🔄 Запуск: ПРАЙС ПОД ЗАКАЗ (основной)\n")
        run_async_task(run_send_order_price("main"))
    else:
        messagebox.showwarning("Подождите", "Уже выполняется задача!")


def start_send_order_test():
    if not is_running:
        disable_buttons()
        append_log("🔄 Запуск: ПРАЙС ПОД ЗАКАЗ (тест)\n")
        run_async_task(run_send_order_price("test"))
    else:
        messagebox.showwarning("Подождите", "Уже выполняется задача!")


def start_refresh_prices():
    if not is_running:
        disable_buttons()
        append_log("🔄 Запуск: ОБНОВИТЬ ЦЕНЫ ОПТ\n")
        run_async_task(run_refresh_stock_price())
    else:
        messagebox.showwarning("Подождите", "Уже выполняется задача!")


def start_update_remains():
    if not is_running:
        disable_buttons()
        append_log("🔄 Запуск: ПРОСТАВИТЬ ЦЕНЫ В ОСТАТКАХ\n")
        run_async_task(run_update_remains())
    else:
        messagebox.showwarning("Подождите", "Уже выполняется задача!")
        
def start_upload_orders():
    if not is_running:
        disable_buttons()
        append_log("🔄 Запуск: ВЫГРУЗКА ПОСТАВЩИКОВ\n")
        run_async_task(run_upload_orders())
    else:
        messagebox.showwarning("Подождите", "Уже выполняется задача!")


# === Блокировка кнопок во время выполнения ===
def disable_buttons():
    for btn in buttons:
        btn.configure(state='disabled')


def enable_buttons():
    for btn in buttons:
        btn.configure(state='normal')


# === GUI ===
root = tk.Tk()
root.title("🔧 Mobilo4ka — Панель управления прайсами")
root.geometry("1000x700")
root.resizable(True, True)

# === Стили ttk ===
style = ttk.Style()
style.theme_use('clam')

# Общие цвета
bg_color = "#f8f9fa"
accent_main = "#2ecc71"
accent_test = "#3498db"
accent_action = "#e67e22"
disabled_fg = "#a0a0a0"

style.configure("TFrame", background=bg_color)
style.configure("TLabel", background=bg_color)
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)

style.map("Main.TButton",
    foreground=[("active", "white"), ("!disabled", "white")],
    background=[("active", "#27ae60"), ("!disabled", accent_main)],
)
style.map("Test.TButton",
    foreground=[("active", "white"), ("!disabled", "white")],
    background=[("active", "#2980b9"), ("!disabled", accent_test)],
)
style.map("Action.TButton",
    foreground=[("active", "white"), ("!disabled", "white")],
    background=[("active", "#d35400"), ("!disabled", accent_action)],
)

# === Заголовок ===
title_label = tk.Label(
    root,
    text="🎯 Mobilo4ka — Обновление прайсов",
    font=("Helvetica", 16, "bold"),
    fg="navy",
    bg=bg_color
)
title_label.pack(pady=10)

# === Фрейм с кнопками ===
frame = tk.Frame(root, bg=bg_color)
frame.pack(pady=10, padx=20, anchor="center")

# === Кнопки ===
buttons = []

btn1 = ttk.Button(
    frame, text="📤 Прайс по наличию (основной)",
    command=start_send_stock_main, style="Main.TButton",
    width=40
)
btn1.grid(row=0, column=0, padx=5, pady=5)
buttons.append(btn1)

btn2 = ttk.Button(
    frame, text="🧪 Прайс по наличию (тест)",
    command=start_send_stock_test, style="Test.TButton",
    width=40
)
btn2.grid(row=0, column=1, padx=5, pady=5)
buttons.append(btn2)

btn3 = ttk.Button(
    frame, text="📦 Прайс под заказ (основной)",
    command=start_send_order_main, style="Main.TButton",
    width=40
)
btn3.grid(row=1, column=0, padx=5, pady=5)
buttons.append(btn3)

btn4 = ttk.Button(
    frame, text="🔬 Прайс под заказ (тест)",
    command=start_send_order_test, style="Test.TButton",
    width=40
)
btn4.grid(row=1, column=1, padx=5, pady=5)
buttons.append(btn4)

btn5 = ttk.Button(
    frame, text="💰 Обновить цены опт",
    command=start_refresh_prices, style="Action.TButton",
    width=40
)
btn5.grid(row=2, column=0, padx=5, pady=5)
buttons.append(btn5)

btn6 = ttk.Button(
    frame, text="🧮 Проставить остатки",
    command=start_update_remains, style="Action.TButton",
    width=40
)
btn6.grid(row=2, column=1, padx=5, pady=5)
buttons.append(btn6)
btn7 = ttk.Button(
    frame, text="👩🏻‍💻 Выгрузить поставщиков",
    command=start_upload_orders, style="Action.TButton",
    width=40
)
btn7.grid(row=3, column=0, padx=5, pady=5)
buttons.append(btn7)


frame.grid_columnconfigure(0, weight=1, uniform="group")
frame.grid_columnconfigure(1, weight=1, uniform="group")
frame.grid_rowconfigure(0, weight=1, uniform="group")
frame.grid_rowconfigure(1, weight=1, uniform="group")
frame.grid_rowconfigure(2, weight=1, uniform="group")

# === Конфигурация поставщиков (редактор) ===
cfg_frame = tk.Frame(root, bg=bg_color)
cfg_frame.pack(fill="x", padx=20, pady=(10, 0))

cfg_label = tk.Label(cfg_frame, text="⚙️ Конфигурация поставщиков:", bg=bg_color)
cfg_label.pack(side="left")

edit_btn = ttk.Button(cfg_frame, text="Редактировать конфиг", command=show_config_editor, width=18)
edit_btn.pack(side="right", padx=6)
open_btn = ttk.Button(cfg_frame, text="Открыть в редакторе", command=open_config_in_editor, width=18)
open_btn.pack(side="right", padx=6)

# === Логи ===
log_label = tk.Label(
    root,
    text="📜 Логи выполнения:",
    font=("Helvetica", 10, "bold"),
    fg="#333",
    bg=bg_color
)
log_label.pack(anchor="w", padx=20, pady=(10, 0))

log_area = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    height=18,
    state='disabled',
    font=("Courier New", 9),
    bg="#ffffff",
    fg="#2c3e50",
    relief="flat",
    borderwidth=2,
    highlightbackground="#dcdcdc",
    highlightcolor="#bdc3c7",
    highlightthickness=1
)
log_area.pack(padx=20, pady=5, fill="both", expand=True)

# === Кнопка очистки ===
clear_btn = ttk.Button(
    root, text="🗑 Очистить логи",
    command=lambda: log_area.configure(state='normal') or log_area.delete(1.0, tk.END) or log_area.configure(state='disabled'),
    width=20
)
clear_btn.pack(pady=5, padx=20, anchor="center")

# === Подвал ===
footer = tk.Label(
    root,
    text=f"© Mobilo4ka • GUI Tool • v1.0 — Конфиг: {SUPPLIERS_PATH.name}",
    fg="#7f8c8d",
    font=("Arial", 8),
    bg=bg_color
)
footer.pack(side="bottom", pady=8)

# === Корректное завершение бота при выходе ===
def on_close():
    if is_running:
        if not messagebox.askyesno("Завершение", "Идёт выполнение задачи. Завершить?"):
            return
    append_log("⏹ Завершение работы GUI...\n")
    try:
        if bot:
            try:
                asyncio.run(bot.close())
            except Exception:
                try:
                    asyncio.run(bot.session.close())
                except Exception:
                    pass
    except Exception:
        pass
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

# Запуск GUI
if __name__ == "__main__":
    append_log("✅ GUI запущено. Готов к работе.\n")
    root.mainloop()