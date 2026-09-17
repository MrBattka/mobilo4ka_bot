from pyrogram import Client
from config.settings import CREDENTIALS_FILE, PHONE_2, API_HASH, API_ID


# ID канала, который нужно проверить
target_chat_id = -1001245719268

def main():
    # Создаем клиент и оборачиваем в with для корректного запуска и остановки
    with Client("my_session", api_id=API_ID, api_hash=API_HASH) as app:
        try:
            # Получаем информацию о чате/канале
            chat = app.get_chat(target_chat_id)
            
            # Выводим название и юзернейм (если есть)
            print(f"Название канала: {chat.title}")
            if chat.username:
                print(f"Юзернейм: @{chat.username}")
            else:
                print("У канала нет публичного юзернейма.")
                
        except Exception as e:
            print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
