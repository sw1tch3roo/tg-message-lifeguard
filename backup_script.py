from telethon import TelegramClient, events, sync
from telethon.tl.types import InputChannel, PeerChannel
from telethon.tl.types import Channel
import time

api_id = API_ID
api_hash = API_HASH

client = TelegramClient('session_name', api_id, api_hash)
client.start()

group = client.get_entity(PeerChannel(GROUP_CHAT_ID))

messages = client.get_admin_log(group)

file1 = open("dump.json","w") 
c = 0
m = 0

# Минимальный ID для сообщений. Начинаем с None, чтобы загрузить последние сообщения.
max_id = 0
limit_per_request = 100  # Количество событий за один запрос

while True:
    # Загружаем события с учетом max_id и лимита
    events = list(client.iter_admin_log(group, max_id=max_id, limit=limit_per_request, delete=True))

    if not events:
        print("Загрузка завершена, новых сообщений нет.")
        break

    # Обрабатываем сообщения
    for event in events:
        if event.deleted_message:  # Проверяем, если это событие удаления сообщения
            print(f"Dumping message {c} (ID: {event.old.id}, Date: {event.old.date})")
            file1.write(event.old.to_json() + ",")  # Записываем сообщение в файл
            c += 1

            if event.old.media:  # Если есть медиафайлы, скачиваем их
                m += 1
                client.download_media(event.old.media, str(event.old.id))
                print(f"Dumped media {m}")

            time.sleep(0.1)  # Небольшая пауза между запросами для избежания блокировки

    # Обновляем max_id для следующего запроса, чтобы загружать более старые сообщения
    max_id = events[-1].id

file1.close()