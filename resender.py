import json
import time
import glob
from telethon import TelegramClient
from telethon.tl.types import PeerChannel
from datetime import datetime
import asyncio

async def main():
    with open("dump.json", "r") as file:
        content = json.load(file)
        content = sorted(content, key=lambda x: x["date"])

        api_id = API_ID
        api_hash = API_HASH
        chat_id = GROUP_CHAT_ID

        client = TelegramClient('session_name', api_id, api_hash)
        await client.start()

        group = await client.get_entity(PeerChannel(int(chat_id)))

        for msg in content:
            message_id = msg["id"]
            message = msg.get("message", "")
            has_media = msg.get('media', None) is not None
            has_message = message != ""
            date = datetime.fromisoformat(msg["date"]).strftime("%Y %b %d, %H:%M")

            print(f"{message_id} {message}, {date}, has_media: {has_media}")

            if has_message:
                message = str(date) + "\n\n" + str(message)
            else:
                message = str(date)

            did_send_media_msg = False

            if has_media:
                file_names = glob.glob(f"{message_id}.*")
                for file_name in file_names:
                    print(f"Sending Media: {file_name}")
                    try:
                        await client.send_file(entity=group, file=file_name, caption=message, silent=True)
                        did_send_media_msg = True
                    except Exception as e:
                        print(f"Error sending media {file_name}: {str(e)}")

            if has_message or not did_send_media_msg:
                print(f"Sending Message: {message}")
                try:
                    await client.send_message(entity=group, message=message, silent=True)
                except Exception as e:
                    print(f"Error sending message: {str(e)}")

            time.sleep(2)

asyncio.run(main())