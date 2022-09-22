from os import environ
from time import sleep
from typing import Any, Mapping, NamedTuple

from loguru import logger
from requests import get

MSG_DELAY = int(environ["MSG_DELAY"])
SHOUTBOX_URL = environ["SHOUTBOX_URL"]
HISTORY_FILE_PATH = "history"
FLOOD_PREVENTION_DELAY_SECONDS = 2

TELEGRAM_API = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
BOT_TOKEN = environ["BOT_TOKEN"]
GROUPS = environ["GROUPS"]
VALID_TELEGRAM_CONFIG = BOT_TOKEN and GROUPS


class Update(NamedTuple):
    id: int
    user: str
    content: str


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


def get_latest_id() -> int:
    with open(HISTORY_FILE_PATH) as histfile:
        previous_msg_id = histfile.read().strip()
    return int(previous_msg_id) if previous_msg_id.isnumeric() else 0


def store_latest_id(id: int) -> None:
    with open(HISTORY_FILE_PATH, "w") as histfile:
        histfile.write(str(id))


def get_updates() -> list[Update]:
    resp = get(SHOUTBOX_URL)
    raw_updates = resp.json()["all"][::-1]
    updates = map(parse_update, raw_updates)
    return list(sorted(updates, key=lambda update: update.id))


def parse_update(raw_update: Mapping[str, Any]) -> Update:
    id = int(raw_update["id"])
    user = raw_update["username"]
    content = raw_update["shout"]
    logger.info(f"[{id}] {user}: {content}")
    return Update(id, user, content)


def select_new_updates(updates: list[Update], latest_id: int) -> list[Update]:
    return [update for update in updates if update.id > latest_id]


def send_update(user: str, content: str) -> None:
    for group in GROUPS.split(","):
        get(TELEGRAM_API.format(BOT_TOKEN, group, f"{user}: {content}"))
    sleep(FLOOD_PREVENTION_DELAY_SECONDS)  # Dirty flood prevention


if __name__ == "__main__":
    main()
