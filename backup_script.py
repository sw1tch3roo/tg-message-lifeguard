import os
from telethon import TelegramClient, events, sync
from telethon.tl.types import InputChannel, PeerChannel
from telethon.tl.types import Channel
import time

# Запрашиваем данные у пользователя
api_id = int(input("Введите ваш api_id: "))
api_hash = input("Введите ваш api_hash: ")

session_name = 'session_name'
session_file = f"{session_name}.session"

# Удаляем файл сессии, если он существует
if os.path.exists(session_file):
    os.remove(session_file)
    print(f"Удален существующий файл сессии: {session_file}")

# Инициализация клиента
client = TelegramClient('session_name', api_id, api_hash)
client.start()

def export_messages(group_id, mode, min_id=0, max_id=0):
    group = client.get_entity(PeerChannel(group_id))

    # Проверяем, существует ли файл, чтобы дописать, а не перезаписать
    file_mode = 'a' if os.path.exists("dump.json") else 'w'
    file1 = open("dump.json", file_mode)

    c = 0  # Счётчик текстовых сообщений
    m = 0  # Счётчик медиа

    limit_per_request = 100  # Количество событий за запрос

    try:
        while True:
            events = list(client.iter_admin_log(
                group,
                min_id=min_id,
                max_id=max_id,
                limit=limit_per_request,
                delete=True  # Интересуемся только удалёнными сообщениями
            ))

            if not events:
                print("Загрузка завершена, новых сообщений нет.")
                break

            # Фильтруем и обрабатываем сообщения
            for event in events:
                if event.deleted_message and event.old.id >= min_id:  # Проверяем, удалено ли сообщение и соответствует ли min_id
                    if mode == 1:  # Экспорт всех текстов и медиа
                        file1.write(event.old.to_json() + ",")  # Записываем сообщение в файл
                        c += 1
                        print(f"Сохранено сообщение {c} (ID: {event.old.id}, Дата: {event.old.date})")

                        if event.old.media:  # Если есть медиа, загружаем
                            m += 1
                            client.download_media(event.old.media, str(event.old.id))
                            print(f"Сохранен медиафайл {m} (ID: {event.old.id}, Дата: {event.old.date})")

                    elif mode == 2 and event.old.media:  # Экспорт только медиа
                        m += 1
                        client.download_media(event.old.media, str(event.old.id))
                        print(f"Сохранен медиафайл {m} (ID: {event.old.id}, Дата: {event.old.date})")

                    elif mode == 3 and not event.old.media:  # Экспорт только текстовых сообщений
                        file1.write(event.old.to_json() + ",")  # Записываем текстовое сообщение в файл
                        c += 1
                        print(f"Сохранено текстовое сообщение {c} (ID: {event.old.id}, Дата: {event.old.date})")

                    time.sleep(0.1)  # Небольшая пауза, чтобы избежать блокировки

            max_id = events[-1].id - 1  # Исключаем последнее полученное событие из следующего запроса

            # Если последнее обработанное событие меньше min_id, завершаем цикл
            if max_id < min_id:
                print("Достигнут нижний предел ID.")
                break

    finally:
        file1.close()

# Запрашиваем дополнительные данные у пользователя
export_mode = int(input("Введите режим экспорта (1 - все, 2 - только медиа, 3 - только текст): "))
min_message_id = int(input("Введите минимальный ID сообщения (0 для начала с первого): "))
max_message_id = int(input("Введите максимальный ID сообщения (0 для получения всех): "))
group_id = int(input("Введите ID группы или канала: "))

# Экспортируем сообщения
export_messages(group_id, export_mode, min_id=min_message_id, max_id=max_message_id)