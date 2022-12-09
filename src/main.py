from os import environ
from time import sleep

from loguru import logger
from requests import get, post

from history import get_latest_id, store_latest_id
from updates import get_updates, select_new_updates

MSG_DELAY = int(environ["MSG_DELAY"])
FLOOD_PREVENTION_DELAY_SECONDS = 2

TELEGRAM_API = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
BOT_TOKEN = environ.get("BOT_TOKEN")
GROUPS = environ.get("GROUPS")
VALID_TELEGRAM_CONFIG = BOT_TOKEN and GROUPS

WEBHOOKS = environ.get("WEBHOOKS")
AVATAR_URL = environ.get("AVATAR_URL")
VALID_DISCORD_CONFIG = WEBHOOKS is not None


def main() -> None:
    if not VALID_TELEGRAM_CONFIG and not VALID_DISCORD_CONFIG:
        logger.error("Not valid config for either Telegram nor Discord!")
        return
    while not sleep(MSG_DELAY):
        shoutbox_monitor()


def shoutbox_monitor() -> None:
    updates = get_updates()
    new_updates = select_new_updates(updates, get_latest_id())
    for update in new_updates:
        store_latest_id(update.id)
        send_update(update.user, update.content)


def send_update(user: str, content: str) -> None:
    if VALID_TELEGRAM_CONFIG:
        send_update_telegram(user, content)
    if VALID_DISCORD_CONFIG:
        send_update_discord(user, content)
    sleep(FLOOD_PREVENTION_DELAY_SECONDS)  # Dirty flood prevention


def send_update_telegram(user: str, content: str) -> None:
    for group in GROUPS.split(","):
        get(TELEGRAM_API.format(BOT_TOKEN, group, f"{user}: {content}"))


def send_update_discord(user: str, content: str) -> None:
    for webhook_url in WEBHOOKS.split(","):
        update_payload = {
            "content": content,
            "username": user,
            "avatar_url": AVATAR_URL,
        }
        post(webhook_url, json=update_payload)


if __name__ == "__main__":
    main()
