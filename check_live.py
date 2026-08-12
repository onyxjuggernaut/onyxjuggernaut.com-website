import asyncio
import json
import os

from TikTokLive import TikTokLiveClient

# Your TikTok username
USERNAME = "@onyxjuggernaut"

STATUS_FILE = "status.json"


async def check_live() -> bool:
    client = TikTokLiveClient(unique_id=USERNAME)
    try:
        return await client.is_live()
    except Exception as e:
        print(f"Error checking live status, assuming offline: {e}")
        return False


def main():
    is_live = asyncio.run(check_live())

    current = {"live": False}
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, "r") as f:
                current = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass

    if current.get("live") != is_live:
        with open(STATUS_FILE, "w") as f:
            json.dump({"live": is_live}, f, indent=2)
            f.write("\n")
        print(f"Status changed -> live: {is_live}")
    else:
        print(f"Status unchanged -> live: {is_live}")


if __name__ == "__main__":
    main()
