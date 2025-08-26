# Meshtastic Weather Bot 🤖🌦️

A simple Python bot that listens for a trigger word on a Meshtastic channel and replies with the current weather for a specified location.

This script uses the [Meshtastic Python CLI](https://meshtastic.org/docs/software/python/cli/installation) to listen for messages and sends weather data fetched from the free and open-source weather service [wttr.in](https://wttr.in).

***

## How It Works

The script continuously listens for incoming text messages on a designated Meshtastic channel. When it detects a message containing a specific `TRIGGER_WORD` (e.g., "weather"), it sends an HTTP request to `wttr.in` to get the current weather conditions for a pre-configured `LOCATION`. The nicely formatted weather report is then broadcast back to the same Meshtastic channel.

***

## Features

-   **Real-time Weather**: Fetches up-to-date weather data on demand.
-   **Easy to Use**: Simply run the script, and it handles the rest.
-   **Customizable**: Easily change the location, trigger word, and Meshtastic channel by editing the configuration variables.
-   **Lightweight**: Minimal dependencies, relying only on the `requests` library and the Meshtastic CLI.
-   **Optional Prefix**: Add a custom prefix (like your node's name) to all replies for easy identification.

***

## Prerequisites

Before you begin, ensure you have the following installed and configured:

1.  **Python 3.x**: Make sure you have a modern version of Python installed.
2.  **Meshtastic Python CLI**: The script relies on the CLI to communicate with your node. You can install it via pip:
    ```shell
    pip install --upgrade meshtastic
    ```
3.  **A Meshtastic Node**: A physical Meshtastic device must be connected to the computer running the script (e.g., via USB) and properly configured. Ensure you can communicate with it using commands like `meshtastic --nodes`.

***

## Installation & Setup

1.  **Download the Script**: Clone this repository or simply download the Python script file to your computer.

2.  **Install Dependencies**: The script requires the `requests` library to fetch weather data. Install it using pip:
    ```shell
    pip install requests
    ```

3.  **Configure the Script**: Open the Python script in a text editor and modify the variables in the **Configuration** section at the top of the file:

    ```python
    # --- Configuration ---

    # Set the Meshtastic channel index you want to use (0 is usually the PRIMARY).
    CHANNEL_INDEX = 0

    # Set the location for the weather report.
    LOCATION = "San Juan,PR"

    # Set the word that triggers the weather report. Case-insensitive.
    TRIGGER_WORD = "weather"
    ```
    -   `CHANNEL_INDEX`: The channel you want the bot to listen and reply on. `0` is the default `Primary` channel.
    -   `LOCATION`: The city, region, or landmark for which you want weather reports.
    -   `TRIGGER_WORD`: The keyword the bot will look for in messages.

***

## Usage

1.  Open your terminal or command prompt.
2.  Navigate to the directory where you saved the script.
3.  Run the script (replace `your_script_name.py` with the actual filename):
    ```shell
    python your_script_name.py
    ```
4.  The script will first ask for an optional prefix. You can type something like `[WeatherBot]` and press Enter, or just press **Enter** for no prefix.
    ```
    Enter a custom prefix for replies (or press Enter for none): [Bot]
    ```
5.  The bot is now active and listening for your trigger word on the configured channel.
    ```
    Starting Meshtastic weather bot...
    Listening on channel index 0 for trigger word: 'weather'
    ```
6.  From another node on the mesh, send a message containing the trigger word (e.g., "what is the weather?"). The bot will detect it, fetch the data, and send a reply.
7.  To stop the bot, press `Ctrl+C` in the terminal.

### Example Interaction

> **Node A sends:** `can I get a weather update`
>
> **Bot's terminal shows:**
> ```
> Trigger word received. Fetching weather...
> Sending weather update:
> [Bot] San Juan: 🌦️ +28°C, ↑13km/h, Humidity: 89%
> ```
>
> **Node A (and all nodes on the channel) receives:** `[Bot] San Juan: 🌦️ +28°C, ↑13km/h, Humidity: 89%`

***

## Troubleshooting

-   **`Error: 'meshtastic' command not found`**: This means the Meshtastic Python CLI is either not installed or not in your system's PATH. Follow the installation steps in the [Prerequisites](#prerequisites) section.

-   **`Error: Failed to fetch weather data`**: The script could not connect to `wttr.in`. Check the internet connection on the computer running the bot. The service may also be temporarily unavailable.

-   **Bot doesn't respond to messages**:
    -   Ensure your Meshtastic node is properly connected to the computer.
    -   Verify that the `CHANNEL_INDEX` in the script matches the channel you are sending messages on.
    -   Confirm that the message you are sending contains the exact `TRIGGER_WORD` (note: it is not case-sensitive).

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.
