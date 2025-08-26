import subprocess
import sys
import requests

# --- Configuration ---

# Set the Meshtastic channel index you want to use (0 is usually the PRIMARY).
CHANNEL_INDEX = 0

# Set the location for the weather report.
LOCATION = "San Juan,PR"

# Set the word that triggers the weather report. Case-insensitive.
TRIGGER_WORD = "weather"

# --- Functions ---

def get_weather():
    """Fetches the weather from wttr.in and returns it as a formatted string."""
    # The format shows Location, Condition, Temperature, Wind, and Humidity.
    url = f"https://wttr.in/{LOCATION}?format=%l:%c+%t,+%w,+Humidity:%h&u"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to fetch weather data: {e}", file=sys.stderr)
        return None

def send_meshtastic_message(message, channel_index):
    """Sends a message using the meshtastic CLI."""
    try:
        command = ["meshtastic", "--ch-index", str(channel_index), "--sendtext", message]
        subprocess.run(command, check=True, capture_output=True, text=True, shell=True)
        print("Sending weather update:")
        print(message)
    except FileNotFoundError:
        print("Error: 'meshtastic' command not found.", file=sys.stderr)
        print("Please ensure the Meshtastic CLI is installed and in your system's PATH.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to send message with meshtastic: {e.stderr}", file=sys.stderr)

# --- Main Script Logic ---

def main():
    """Main function to listen for triggers and respond."""
    # Get the custom prefix from the user
    custom_prefix = input("Enter a custom prefix for replies (or press Enter for none): ")

    print(f"Starting Meshtastic weather bot...")
    print(f"Listening on channel index {CHANNEL_INDEX} for trigger word: '{TRIGGER_WORD}'")

    listen_command = ["meshtastic", "--ch-index", str(CHANNEL_INDEX), "--listen"]

    try:
        # Start the meshtastic listener process
        process = subprocess.Popen(listen_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', shell=True)

        # Read output line by line as it comes in
        for line in iter(process.stdout.readline, ''):
            # Check if the line is a text message containing the trigger word
            if 'text:' in line.lower() and TRIGGER_WORD in line.lower():
                print("Trigger word received. Fetching weather...")
                weather_msg = get_weather()
                if weather_msg:
                    final_msg = f"{custom_prefix} {weather_msg}" if custom_prefix else weather_msg
                    send_meshtastic_message(final_msg, CHANNEL_INDEX)

    except FileNotFoundError:
        print("Error: 'meshtastic' command not found. Please ensure it is installed and in your PATH.", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nBot stopped by user. Exiting.")
        process.terminate()

if __name__ == "__main__":
    main()