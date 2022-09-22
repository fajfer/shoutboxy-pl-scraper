from os import environ
from time import sleep
from typing import Any, Mapping, NamedTuple

from loguru import logger
from requests import get
from telegram.ext import CallbackContext, Updater

BOT_TOKEN = environ["BOT_TOKEN"]
MSG_DELAY = int(environ["MSG_DELAY"])
SHOUTBOX_URL = environ["SHOUTBOX_URL"]
GROUPS = environ["GROUPS"].split(",")
HISTORY_FILE_PATH = "history"
FLOOD_PREVENTION_DELAY_SECONDS = 2


class Update(NamedTuple):
    id: int
    user: str
    content: str


def main() -> None:
    updater = Updater(token=BOT_TOKEN, use_context=True)
    updater.job_queue.run_repeating(shoutbox_monitor, MSG_DELAY)
    updater.start_polling()
    updater.idle()


def shoutbox_monitor(context: CallbackContext) -> None:
    updates = get_updates()
    new_updates = select_new_updates(updates, get_latest_id())
    for update in new_updates:
        store_latest_id(update.id)
        send_update(context, update)


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


def send_update(context: CallbackContext, update: Update) -> None:
    for group in GROUPS:
        context.bot.send_message(group, f"{update.user}: {update.content}")
    sleep(FLOOD_PREVENTION_DELAY_SECONDS)  # Dirty anti-flood prevention


if __name__ == "__main__":
    main()
