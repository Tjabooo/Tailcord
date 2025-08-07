from dotenv import load_dotenv
import requests
import json
import time
import os

load_dotenv()

DISCORD_API_URL = 'https://discord.com/api/v9/users'
TAILSCALE_STATUS_COMMAND = 'tailscale status --json'
SLEEP_INTERVAL = 10
TOKEN = os.getenv('TOKEN')
USER_ID = os.getenv('USER_ID')
NODE_KEY_1 = os.getenv('NODE_KEY_1')
NODE_KEY_2 = os.getenv('NODE_KEY_2')
NODE_KEY_3 = os.getenv('NODE_KEY_3')

headers = {
    'authorization': TOKEN
}

def get_discord_user_profile():
    response = requests.get(f'{DISCORD_API_URL}/{USER_ID}/profile?with_mutual_guilds=false&with_mutual_friends_count=false', headers=headers)
    response.raise_for_status()
    user_data = response.json().get("user")
    bio = user_data.get("bio")
    return bio

def get_tailscale_status():
    tailscale_log = os.popen(TAILSCALE_STATUS_COMMAND).read()
    return json.loads(tailscale_log)

def update_discord_status(windows, linux, laptop, rest):
    bio_update = f'{rest}\n\n> system status -\n> Desktop (Win11): {windows}\n> Laptop (Arch): {linux}\n> Laptop (Win11): {laptop}'
    response = requests.patch(f'{DISCORD_API_URL}/@me/profile', headers=headers, json={'bio': bio_update})
    response.raise_for_status()
    return response

def main():
    while True:
        discord_bio = get_discord_user_profile()
        windows_status, linux_status, laptop_status = map(lambda x: x.split(" ")[-1], discord_bio.split("\n")[3:6])
        tailscale_log = get_tailscale_status()
        windows, linux, laptop = map(lambda key: "Online ✅" if tailscale_log['Peer'][key]['Online'] else "Offline ❌", [
            NODE_KEY_1,
            NODE_KEY_2,
            NODE_KEY_3
        ])

        if any(status.split(" ")[0] != current_status for status, current_status in zip([windows, linux, laptop], [windows_status, linux_status, laptop_status])):
            rest = discord_bio.split("> system status -")[0].rstrip()
            response = update_discord_status(windows, linux, laptop, rest)
            print(response, response.content)

        time.sleep(SLEEP_INTERVAL)

if __name__ == "__main__":
    main()
