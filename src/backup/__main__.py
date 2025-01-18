"""
This module handles the export of deleted Telegram messages and media using Telethon.
It supports various export model based on user inputs,
including exporting all deleted messages, media only, or text-only messages.
"""

import os
import asyncio
from telethon import TelegramClient
from telethon.tl.types import PeerChannel
from telethon.errors import RPCError

# Requesting user credentials
api_id: int = int(input("Enter your api_id: "))
api_hash: str = input("Enter your api_hash: ")

session_name: str = "session_name"
session_file: str = f"{session_name}.session"

# Set the output folder
output_folder: str = "backup_will_be_inside_me"
os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

# Remove session file if it exists
if os.path.exists(session_file):
    os.remove(session_file)
    print(f"Existing session file removed: {session_file}")

# Initialize Telegram client
client: TelegramClient = TelegramClient(session_name, api_id, api_hash)
client.start()


async def export_messages(
    target_group_id: int,
    mode: int,
    min_id: int = 0,
    max_id: int = 0,
) -> None:
    """
    Exports messages from a Telegram group or channel.

    :param group_id: ID of the Telegram group or channel.
    :param mode: Export mode (1 - all, 2 - media only, 3 - text only).
    :param min_id: Minimum message ID to export.
    :param max_id: Maximum message ID to export.
    """
    group: PeerChannel = await client.get_entity(PeerChannel(target_group_id))
    # Define the dump file path
    dump_file = os.path.join(output_folder, "dump.json")
    # Check if the file exists to append data instead of overwriting
    file_mode: str = "a" if os.path.exists(dump_file) else "w"

    with open(dump_file, file_mode, encoding="utf-8") as dump:
        c: int = 0  # Counter for text messages
        m: int = 0  # Counter for media messages

        limit_per_request: int = 100  # Number of events per request

        try:
            async for event in client.iter_admin_log(
                group,
                min_id=min_id,
                max_id=max_id,
                limit=limit_per_request,
                delete=True,  # Only interested in deleted messages
            ):
                # Filter and process messages
                if event.deleted_message and event.old.id >= min_id:
                    if mode == 1:  # Export all text and media
                        dump.write(event.old.to_json() + ",")
                        c += 1
                        print(
                            f"Saved message {c} (ID: {event.old.id}, Date: {event.old.date})"
                        )

                        if event.old.media:  # Download media if available
                            m += 1
                            await client.download_media(
                                event.old.media,
                                os.path.join(output_folder, str(event.old.id))
                            )
                            print(
                                f"Saved media file {m} (ID: {event.old.id}, Date: {event.old.date})"
                            )

                    elif mode == 2 and event.old.media:  # Export media only
                        m += 1
                        await client.download_media(
                            event.old.media,
                            os.path.join(output_folder, str(event.old.id)))
                        print(
                            f"Saved media file {m} (ID: {event.old.id}, Date: {event.old.date})"
                        )

                    elif mode == 3 and not event.old.media:  # Export text only
                        dump.write(event.old.to_json() + ",")
                        c += 1
                        print(
                            f"Saved text message {c} (ID: {event.old.id}, Date: {event.old.date})"
                        )

                    await asyncio.sleep(0.1)  # Short pause to avoid blocking

            print("Export completed, no new messages found.")

        except RPCError as e:
            print(f"An error occurred: {e}")


# Request additional details from the user
export_mode: int = int(
    input("Enter export mode (1 - all, 2 - media only, 3 - text only): ")
)
min_message_id: int = int(
    input("Enter the minimum message ID (0 to start from the first): ")
)
max_message_id: int = int(
    input("Enter the maximum message ID (0 to retrieve all): ")
)
group_id: int = int(input("Enter the group or channel ID: "))


async def main() -> None:
    """
    Main function to start the export process.
    """
    await client.start()
    await export_messages(
        group_id, export_mode, min_id=min_message_id, max_id=max_message_id
    )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
