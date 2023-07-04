import time
import requests
import pypresence
import psutil

# Replace these with your API endpoint and Discord application client ID
API_ENDPOINT = "https://api.ballisticok.xyz/fortnite/player/YOUR_NAME_HERE/season" # Replace YOUR_NAME_HERE with your epic name
CLIENT_ID = "437180137050734592" # you can change this if you want or leave it to use mine
API_KEY = "YOUR_KEY_HERE" # Replace with your key from https://api.ballisticok.xyz/

# Initialize the Discord Rich Presence client
client = pypresence.Presence(CLIENT_ID)

# Connect to the Discord client
client.connect()

# Set this variable to True if you want to show the activity only when Fortnite is running
show_only_when_fortnite_running = False

while True:
    if not show_only_when_fortnite_running or "FortniteClient-Win64-Shipping.exe" in (
        p.name() for p in psutil.process_iter()
    ):
        try:
            # Make a request to the API and get the response data
            headers = {"api-key": API_KEY}
            response = requests.get(API_ENDPOINT, headers=headers).json()
            data = response["data"]

            # Extract the battle pass level and progress data
            battle_pass_level = data["battlePass"]["level"]
            battle_pass_progress = data["battlePass"]["progress"]

            # Set the state to show the battle pass level
            state = f"Battle Pass Level {battle_pass_level}"
            print(f"Battle Pass Level: {battle_pass_level}")
        except:
            # If there's an error getting data from the API, set the state to "Scanning data files"
            state = "Scanning data files"
            battle_pass_progress = None
            print("Error retrieving data from the API")

        # Set the Discord Rich Presence activity
        activity = {
            "state": state,
            "details": f"Current Level Progress: {battle_pass_progress}%" if battle_pass_progress is not None else None,
            "large_image": "fortnite",
            "large_text": "Fortnite Stats",
            "small_image": "python",
            "small_text": "Made with Python",
        }

        # Update the activity on the Discord client
        client.update(**activity)
        print("Discord Rich Presence updated")
    else:
        # If Fortnite is not running, set the state to "Fortnite is not running"
        activity = {
            "state": "Fortnite is not running",
            "details": None,
            "large_image": "fortnite",
            "large_text": "Fortnite Stats",
            "small_image": "python",
            "small_text": "Made with Python",
        }
        client.update(**activity)
        print("Fortnite is not running")

    # Wait for 15 seconds before updating the activity again
    time.sleep(15)
