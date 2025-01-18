import os
import time
from typing import Optional
from telethon import TelegramClient
from telethon.tl.types import PeerChannel
import asyncio

# Запрашиваем данные у пользователя
api_id: int = int(input("Введите ваш api_id: "))
api_hash: str = input("Введите ваш api_hash: ")

session_name: str = "session_name"
session_file: str = f"{session_name}.session"

# Удаляем файл сессии, если он существует
if os.path.exists(session_file):
    os.remove(session_file)
    print(f"Удален существующий файл сессии: {session_file}")

# Инициализация клиента
client: TelegramClient = TelegramClient(session_name, api_id, api_hash)
client.start()


async def export_messages(
    group_id: int,
    mode: int,
    min_id: int = 0,
    max_id: int = 0,
) -> None:
    group: PeerChannel = await client.get_entity(PeerChannel(group_id))

    # Проверяем, существует ли файл, чтобы дописать, а не перезаписать
    file_mode: str = "a" if os.path.exists("dump.json") else "w"

    with open("dump.json", file_mode) as dump:
        c: int = 0  # Счётчик текстовых сообщений
        m: int = 0  # Счётчик медиа

        limit_per_request: int = 100  # Количество событий за запрос

        try:
            async for event in client.iter_admin_log(
                group,
                min_id=min_id,
                max_id=max_id,
                limit=limit_per_request,
                delete=True,  # Интересуемся только удалёнными сообщениями
            ):
                # фильтруем и обрабатываем сообщения
                if (
                    event.deleted_message and event.old.id >= min_id
                ):  # Проверяем, удалено ли сообщение и соответствует ли min_id
                    if mode == 1:  # Экспорт всех текстов и медиа
                        dump.write(
                            event.old.to_json() + ","
                        )  # Записываем сообщение в файл
                        c += 1
                        print(
                            f"Сохранено сообщение {c} (ID: {event.old.id}, Дата: {event.old.date})"
                        )

                        if event.old.media:  # Если есть медиа, загружаем
                            m += 1
                            await client.download_media(
                                event.old.media, str(event.old.id)
                            )
                            print(
                                f"Сохранен медиафайл {m} (ID: {event.old.id}, Дата: {event.old.date})"
                            )

                    elif mode == 2 and event.old.media:  # Экспорт только медиа
                        m += 1
                        await client.download_media(event.old.media, str(event.old.id))
                        print(
                            f"Сохранен медиафайл {m} (ID: {event.old.id}, Дата: {event.old.date})"
                        )

                    elif (
                        mode == 3 and not event.old.media
                    ):  # Экспорт только текстовых сообщений
                        dump.write(
                            event.old.to_json() + ","
                        )  # Записываем текстовое сообщение в файл
                        c += 1
                        print(
                            f"Сохранено текстовое сообщение {c} (ID: {event.old.id}, Дата: {event.old.date})"
                        )

                    await asyncio.sleep(
                        0.1
                    )  # Небольшая пауза, чтобы избежать блокировки

            print(
                "Загрузка завершена, новых сообщений нет."
            )  # Сообщение после завершения итерации

        except Exception as e:
            print(f"Произошла ошибка: {e}")


# Запрашиваем дополнительные данные у пользователя
export_mode: int = int(
    input("Введите режим экспорта (1 - все, 2 - только медиа, 3 - только текст): ")
)
min_message_id: int = int(
    input("Введите минимальный ID сообщения (0 для начала с первого): ")
)
max_message_id: int = int(
    input("Введите максимальный ID сообщения (0 для получения всех): ")
)
group_id: int = int(input("Введите ID группы или канала: "))


async def main():
    await client.start()
    await export_messages(
        group_id, export_mode, min_id=min_message_id, max_id=max_message_id
    )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
