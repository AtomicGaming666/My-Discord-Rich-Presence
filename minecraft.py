import time
import requests
import pypresence
import psutil
import logging

logging.basicConfig(filename='error.log', level=logging.ERROR)

# Replace this with your UUID
UUID = "YOUR_MC_UUID"

# Replace these with your API endpoint
SERVERTAP_API_ENDPOINT = "YOUR_SERVER_TAP_API_USER"
SERVERTAP_API_KEY = "OUR_SERVER_TAP_KEY"

# You can leave this
CLIENT_ID = "467874114653388800"

# Initialize the Discord Rich Presence client
client = pypresence.Presence(CLIENT_ID)

# Connect to the Discord client
client.connect()
print("Connected to Discord client.")


def is_game_running():
    for process in psutil.process_iter(['name']):
        if process.info['name'] == 'javaw.exe':
            return True
    return False


def get_player_stats():
    try:
        # Make a request to the ServerTap API to get the player's data
        headers = {"Authorization": f"{SERVERTAP_API_KEY}"}
        response = requests.get(f"{SERVERTAP_API_ENDPOINT}/players/{UUID}", headers=headers)
        response.raise_for_status()  # Raise an exception if there was an HTTP error
        print("Data received from ServerTap API.")

        # Extract the relevant player stats
        player_data = response.json()
        health = int(player_data["health"])
        hunger = int(player_data["hunger"])
        saturation = int(player_data["saturation"])
        balance = player_data["balance"]
        location = player_data["location"]

        # Extract X, Y, Z coordinates from location and remove decimals
        x = int(location[0])
        y = int(location[1])
        z = int(location[2])

        # Return a dictionary with the relevant stats
        return {"health": health, "hunger": hunger, "saturation": saturation, "balance": balance, "x": x, "y": y, "z": z}

    except requests.exceptions.RequestException as e:
        logging.error(f"Error getting player stats: {e}")
        print(f"Error getting player stats: {e}")
        return None

    except (ValueError, KeyError) as e:
        logging.error(f"Error parsing player stats: {e}")
        print(f"Error parsing player stats: {e}")
        return None


def update_discord_presence(stats):
    # Set the state to show the player's stats
    if stats:
        health = stats['health']
        hunger = stats['hunger']
        saturation = stats['saturation']
        balance = stats['balance']
        x = stats['x']
        y = stats['y']
        z = stats['z']

        state = f"Balance: {balance} | X: {x} Y: {y} Z: {z}"
        details = f"Health: {health} | Hunger: {hunger} | Saturation: {saturation}"

        # Set the Discord Rich Presence activity
        activity = {
            "state": state,
            "details": details,
            "large_image": "minecraft",
            "large_text": "Minecraft Stats",
            "small_image": "python",
            "small_text": "Made with Python"
        }

        # Update the activity on the Discord client
        client.update(**activity)
        print("Discord presence updated.")
    else:
        state = "Scanning data files"
        details = None

        # Set the Discord Rich Presence activity for the scanning state
        activity = {
            "state": state,
            "details": details,
            "large_image": "minecraft",
            "large_text": "Minecraft Stats",
            "small_image": "python",
            "small_text": "Made with Python"
        }

        # Update the activity on the Discord client
        client.update(**activity)
        print("Discord presence updated.")


print("Monitoring player stats. Press Ctrl+C to exit.")
while True:
    try:
        if is_game_running():
            print("Getting player stats...")
            stats = get_player_stats()
            if stats:
                health = stats['health']
                hunger = stats['hunger']
                saturation = stats['saturation']
                balance = stats['balance']
                x = stats['x']
                y = stats['y']
                z = stats['z']
                print(f"Player stats:\nHealth: {health}\nHunger: {hunger}\nSaturation: {saturation}\nBalance: {balance}\nLocation: X:{x} Y:{y} Z:{z}")

            update_discord_presence(stats)
            print("Waiting for 15 seconds before updating the activity again.")
        else:
            print("Game is not running. Waiting for 15 seconds...")
        
        # Wait for 15 seconds before updating the activity again
        time.sleep(15)

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")
