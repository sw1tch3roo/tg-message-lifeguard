# [Telegram Backup Tool] TML Documentation

## Overview
This tool allows you to recover deleted messages and media from Telegram channels and groups. It provides features to export all messages, only media files, or only text messages within a specific ID range.

---

## 📦 Setting Up the Environment

### Installing and Configuring a Virtual Environment (venv)
`venv` is an isolated environment for Python projects. It allows you to install dependencies without affecting the global Python installation on your device.

This is especially important when working with multiple projects that require different library versions.

### 💻 How to Create a Virtual Environment

Open the terminal (bash/zsh), which can be done directly inside VS Code.

#### Creating a virtual environment:
```bash
$ python3 -m venv venv
```
Here, `venv` is the directory name that will contain your virtual environment. You can choose any name for this folder.

#### Activating the virtual environment:
**MacOS/Linux:**
```bash
$ source venv/bin/activate
```
**Windows:**
```bash
$ .\venv\Scripts\activate
```

#### Deactivating the virtual environment:
```bash
$ deactivate
```

### 📂 Installing Project Dependencies
Ensure the virtual environment is activated before installing dependencies:
```bash
$ pip3 install -r requirements.txt
```
Once dependencies are installed, you can run the Python scripts.

---

## 🛠️ Using the Backup Module to Recover Data

### Prerequisites
Before starting the recovery process, you need to obtain the following values:
- `api_id`
- `api_hash`
- `group_chat_id`

### 🔑 Steps to Obtain `api_id` and `api_hash`
1. Go to the [Telegram API website](https://my.telegram.org/).
2. Log in with your phone number in the format `+XXXXXXXXXXXX`.
3. Confirm authentication with the 2FA code.
4. Click on **API development tools**.
5. Your `api_id` and `api_hash` will be displayed on the page.

### 🏷️ Obtaining `group_chat_id` or `channel_id` by following the [instructions](https://gist.github.com/nafiesl/4ad622f344cd1dc3bb1ecbe468ff9f8a#get-chat-id-for-a-group-chat).
Follow the provided instructions to obtain these values. Store them securely for the recovery process.

---

## 🚀 Starting the Recovery Process

Run the backup module with the following command:
```bash
$ python -m src.backup
```

The script will prompt you to enter:

- **api_id:** Enter your previously obtained `api_id`.
- **api_hash:** Enter your previously obtained `api_hash`.

### 🔐 Authorization Step

You will be prompted with the following message:
```bash
$ Please enter your phone (or bot token):
```

#### Authentication Methods:
1. **Logging in via personal account (Recommended):**
   - Enter your phone number.
   - Enter your password.
   - Input the 2FA code received from Telegram Service Notifications (TSN).

2. **Using a bot token (Not recommended due to restrictions):**
   - Create a bot via [@BotFather](https://t.me/BotFather).
   - Obtain the API Token.
   - Enter it in the terminal.

⚠️ **Important:** Bot authentication may result in the following error:
```bash
telethon.errors.rpcerrorlist.BotMethodInvalidError: The API access for bot users is restricted.
```
Thus, user account authorization is required.

---

## 📊 Export Modes
You can choose from the following export modes:
- Export **all messages and media**.
- Export **only media files**.
- Export **only text messages**.

### 🔢 Setting Message ID Ranges
- **Minimum message ID:** `0` (start from the very first message).
- **Maximum message ID:** `0` (retrieve all messages).

**Example:**
```bash
min_message_id = 23456
max_message_id = 25673
```
This will recover messages within the specified range.

### 📌 Group or Channel ID
Enter the `group_chat_id` obtained earlier.

---

## 📥 Output and Recovery Management
The recovered media files and `dump.json` will be stored in the `backup_will_be_inside_me` folder, which is automatically created in the working directory during recovery.

**Important:** Each exported media file will be named after the corresponding message ID (the text message IDs will be in the `dump.json`).

If the script is interrupted, use the ID of the last exported message to resume the process. Restart the script and specify the min_message_id equal to the message id.
This allows the script to continue from the specified message ID.

---

## 📺 Monitoring the Process
Once the script is running, monitor the console output to track progress.

