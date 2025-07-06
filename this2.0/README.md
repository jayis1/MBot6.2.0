<div align="center">
</pre>
</details>
</div>

# 

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/discord.py-2.3.2-blue?style=for-the-badge&logo=discord" alt="discord.py Version">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License"></a>
</p>

A self-contained Discord music bot built with Python and `discord.py`. It's designed for easy setup and robust performance, running as a background service using `screen`. The included `launch.sh` script handles the complete setup, including dependency installation, environment configuration, and automatic generation of necessary files like `__init__.py`.

---

## ✨ Features

- ✅ **Self-Contained Installation**: The `launch.sh` script automatically sets up a virtual environment and installs all dependencies.
- ✅ **Background Operation**: Runs in a `screen` session, ensuring the bot stays online.
- ✅ **YouTube Integration**: Play audio from YouTube URLs, playlists, and search queries.
- ✅ **Full Playback Control**: `play`, `pause`, `resume`, `skip`, `stop`.
- ✅ **Queue Management**: `add`, `remove`, `clear`, `shuffle`, and `view queue`.
- ✅ **Audio Controls**: Adjust `volume` and playback `speed`.
- ✅ **Looping**: Toggle looping for the currently playing song.
- ✅ **Auto-Disconnect**: Automatically disconnects from the voice channel after one minute of inactivity.
- ✅ **Admin Commands**: `shutdown` and `restart` the bot remotely.

---

## 🎯 Target Environment

This bot is primarily developed and tested on **Debian 12 (Bookworm)**. The `launch.sh` script includes commands to install dependencies like `ffmpeg` using `apt-get`, which is specific to Debian-based distributions.

It is suitable for deployment in various environments:
-   **Bare Metal**: A dedicated physical machine running Debian 12.
-   **Type 1 Hypervisor**:
    -   **Proxmox VE**: Can be run inside a Virtual Machine (VM) or a Linux Container (LXC).
-   **Type 2 Hypervisor**:
    -   **VirtualBox**, **VMware Workstation/Fusion**: Can be run inside a Debian 12 guest VM.

While it may work on other Linux distributions, you might need to manually install the required system dependencies (`ffmpeg`, `libopus-dev`) using your distribution's package manager.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- `git`
- `ffmpeg` and `libopus-dev` (The setup script will attempt to install these on Debian-based systems).

### ⚙️ Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Make the Launch Script Executable**
    You may need to grant execute permissions to the launch script.
    ```bash
    chmod +x launch.sh
    ```

3.  **Configure the Bot**
    You can configure the bot in one of two ways:

    **Method 1: Using a `.env` file (Recommended)**
    Create a `.env` file by copying the example file:
    ```bash
    cp .env.example .env
    ```
    Now, edit the `.env` file with your credentials using a text editor like `nano`:
    ```bash
    nano .env
    ```
    See the **Configuration Details** section below for more information on what to put in this file.

    **Method 2: Hardcoding in `config.py`**
    If you prefer, you can hardcode your credentials directly into the `config.py` file.
    ```bash
    nano config.py
    ```
    **Note:** This is not recommended, especially if your code is in a public repository.

4.  **Run the Setup Script**
    This command prepares the environment, installs all Python packages, and makes the other scripts executable.
    ```bash
    ./launch.sh setup
    ```

---

## 🤖 Usage

The `launch.sh` script is your control center for the bot.

| Command               | Description                                                              |
| --------------------- | ------------------------------------------------------------------------ |
| `./launch.sh start`   | Starts the bot in a new `screen` session.                                |
| `./launch.sh stop`    | Stops the bot and closes the `screen` session.                           |
| `./launch.sh restart` | Restarts the bot.                                                        |
| `./launch.sh attach`  | Displays recent logs and attempts to attach to the bot's console. See "Known Issues" if the console appears blank. |

---

## 🎵 Commands

The default command prefix is `?`.

<details>
  <summary>Click to view Music Commands</summary>

| Command                          | Description                                      |
| -------------------------------- | ------------------------------------------------ |
| `?join`                          | Joins your current voice channel.                |
| `?leave`                         | Disconnects from the voice channel.              |
| `?search <query>`                | Searches YouTube for a song.                     |
| `?play <URL or search query>`    | Plays a song or adds it to the queue.            |
| `?playlist <URL>`                | Adds a YouTube playlist to the queue.            |
| `?queue`                         | Displays the current song queue.                 |
| `?skip`                          | Skips the current song.                          |
| `?stop`                          | Stops playback and clears the queue.             |
| `?pause`                         | Pauses the music.                                |
| `?resume`                        | Resumes the music.                               |
| `?clear`                         | Clears the song queue.                           |
| `?remove <song number>`          | Removes a specific song from the queue.          |
| `?nowplaying`                    | Shows the currently playing song.                |
| `?volume <0-200>`                | Sets the music volume.                           |
| `?loop`                          | Toggles looping for the current song.            |
| `?speedhigher` / `?speedlower`   | Increases or decreases the playback speed.       |
| `?shuffle`                       | Shuffles the song queue.                         |
</details>

<details>
  <summary>Click to view Admin Commands (Bot Owner Only)</summary>

| Command                             | Description                                      |
| ----------------------------------- | ------------------------------------------------ |
| `?fetch_and_set_cookies <URL>`      | Fetches and sets cookies for `yt-dlp`.           |
| `?shutdown`                         | Shuts down the bot.                              |
| `?restart`                         | Restarts the bot.                                |
</details>

---

## 🔧 Configuration Details

-   **`DISCORD_TOKEN`**: Your Discord bot's authentication token. You can get this from the [Discord Developer Portal](https://discord.com/developers/applications) by creating an application and adding a bot.
-   **`YOUTUBE_API_KEY`**: Your YouTube Data API v3 key. This is required for the `?search` command. You can obtain one from the [Google Cloud Console](https://console.cloud.google.com/apis/library/youtube.googleapis.com).
-   **`BOT_OWNER_ID`**: Your personal Discord User ID. This is used for owner-only commands. To get your ID, enable Developer Mode in Discord's settings, then right-click your username and select "Copy User ID".
-   **`LOG_CHANNEL_ID`**: The ID of the Discord channel where the bot will send logs. Get this by enabling Developer Mode, right-clicking the channel, and selecting "Copy Channel ID".

---

## 📁 Project Structure

<details>
  <summary>Click to view the project structure</summary>

```
.
├── cogs/               # Contains the command modules (cogs) for the bot
│   ├── admin.py
│   ├── music.py
│   └── ...
├── utils/              # Utility scripts and helper functions
│   └── ...
├── .env.example        # Example environment file
├── bot.py              # Main bot script
├── config.py           # Bot configuration loader
├── launch.sh           # Main script for managing the bot
├── requirements.txt    # Python dependencies
└── README.md           # This file
```
</details>

---

## ⁉️ Troubleshooting

-   **Bot is offline or not responding:**
    -   Use `./launch.sh attach` to view the latest logs. If the session is not active, start it with `./launch.sh start`.
    -   Check the `bot.log` file for any errors.
    -   Verify that your `DISCORD_TOKEN` is correct.

-   **No audio is playing:**
    -   Make sure `ffmpeg` is installed correctly. The setup script attempts to install it, but it might fail.
    -   Check the bot's logs for any `ffmpeg` or `opus` related errors.

-   **`?search` command is not working:**
    -   Ensure your `YOUTUBE_API_KEY` is correct and that the YouTube Data API v3 is enabled in your Google Cloud project.

---

## ⚠️ Known Issues

-   **`./launch.sh attach` shows a blank screen:**
    -   When running `attach`, the script is designed to first display the last 1000 lines of `bot.log` and then attempt to attach to the `screen` session.
    -   In some terminal environments (especially non-interactive shells or certain SSH clients), the `screen -r` command may result in a blank or unresponsive window even if the bot is running. You might be able to detach using `Ctrl+A` then `D`.
    -   **Workaround**: To view live logs reliably, open a separate terminal and run:
        ```bash
        tail -f bot.log
        ```

---

## 🐛 Bug Fixes

-   **Log Spam on Leave**: Fixed a bug where the bot would continue to spam logs after the `?leave` command was used. The `nowplaying` update task is now properly cancelled.
-   **Interaction Responded Error**: Fixed a bug where the bot would crash if a user clicked the "queue" button multiple times.
-   **Format Not Available Error**: Fixed a bug where the bot would crash if a requested audio format was not available. The bot now selects the best available audio format.
-   **Nowplaying Channel**: Fixed a bug where the `nowplaying` command would only send messages to the log channel. The bot now sends the message to the channel where the command was invoked.

---

## 🤝 Contributing

Contributions are welcome! If you have a feature request, bug report, or want to improve the code, please feel free to open an issue or submit a pull request.

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Commit your changes (`git commit -m 'Add some feature'`).
4.  Push to the branch (`git push origin feature/YourFeature`).
5.  Open a Pull Request.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
<div align="center">
<details>
  <summary>A wild ninja cow appears!</summary>
<pre>
              ^__^
              (oo)\_______
             (__)\       )\/\
                 ||----w |
                 ||     ||
</pre>
</details>
</div>