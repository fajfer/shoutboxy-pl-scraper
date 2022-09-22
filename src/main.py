from os import environ
from time import sleep

from loguru import logger
from requests import get

from history import get_latest_id, store_latest_id
from updates import get_updates, select_new_updates

MSG_DELAY = int(environ["MSG_DELAY"])
FLOOD_PREVENTION_DELAY_SECONDS = 2

TELEGRAM_API = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
BOT_TOKEN = environ["BOT_TOKEN"]
GROUPS = environ["GROUPS"]
VALID_TELEGRAM_CONFIG = BOT_TOKEN and GROUPS


def main() -> None:
    if not VALID_TELEGRAM_CONFIG:
        logger.error("Not valid config for Telegram!")
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
    for group in GROUPS.split(","):
        get(TELEGRAM_API.format(BOT_TOKEN, group, f"{user}: {content}"))
    sleep(FLOOD_PREVENTION_DELAY_SECONDS)  # Dirty flood prevention


if __name__ == "__main__":
    main()
