import subprocess
import sys
import requests

#Configuration

#Set the Meshtastic channel index you want to use (0 is usually the PRIMARY).
CHANNEL_INDEX = 0

#Add a custom prefix to your weather message. Can be left empty.
CUSTOM_PREFIX = "Saludos:"

#Set the location for the weather report.
LOCATION = "San Juan,PR"

#Set the word that triggers the weather report. Case-insensitive.
TRIGGER_WORD = "test321"

#Functions

def get_weather():
    """Fetches the weather from wttr.in and returns it as a formatted string."""
    # The format shows Location, Condition, Temperature, Wind, and Humidity.
    url = f"https://wttr.in/{LOCATION}?format=%l:%c+%t,Vientos:+%w,+Humidity:%h,Precip:%p&u"
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
        subprocess.run(command, check=True, capture_output=True, text=True)
        print("Sending weather update:")
        print(message)
    except FileNotFoundError:
        print("Error: 'meshtastic' command not found.", file=sys.stderr)
        print("Please ensure the Meshtastic CLI is installed and in your system's PATH.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to send message with meshtastic: {e.stderr}", file=sys.stderr)

#Main

def main():
    """Main function to listen for triggers and respond."""
    print(f"Starting Meshtastic weather bot...")
    print(f"Listening on channel index {CHANNEL_INDEX} for trigger word: '{TRIGGER_WORD}'")

    listen_command = ["meshtastic", "--ch-index", str(CHANNEL_INDEX), "--listen"]

    try:
        # Start the meshtastic listener process
        process = subprocess.Popen(listen_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')

        # Read output line by line as it comes in
        for line in iter(process.stdout.readline, ''):
            # Check if the line is a text message containing the trigger word
            if 'text:' in line.lower() and TRIGGER_WORD in line.lower():
                print("Trigger word received. Fetching weather...")
                weather_msg = get_weather()
                if weather_msg:
                    final_msg = f"{CUSTOM_PREFIX} {weather_msg}" if CUSTOM_PREFIX else weather_msg
                    send_meshtastic_message(final_msg, CHANNEL_INDEX)

    except FileNotFoundError:
        print("Error: 'meshtastic' command not found. Please ensure it is installed and in your PATH.", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nBot stopped by user. Exiting.")
        process.terminate()

if __name__ == "__main__":
    main()