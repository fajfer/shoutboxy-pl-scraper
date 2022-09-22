from os import environ
from time import sleep

from loguru import logger
from requests import get
from telegram.ext import CallbackContext, Updater


def send_message(
    context: CallbackContext, author: str, message: str, groups: list[str]
) -> None:
    for group in groups.split(","):
        context.bot.send_message(group, f"{author}: {message}")
        sleep(2)  # Dirty telegram anti-flood prevention


def tg_shoutbox_monitor(context: CallbackContext) -> None:
    with open("history") as histfile:
        old_msg_id = histfile.read()
    resp = get(environ["SHOUTBOX_URL"])
    messages = resp.json()["all"]
    for message in messages[::-1]:
        with open("history") as histfile:
            old_msg_id = histfile.read()
            try:
                int(old_msg_id)
            except ValueError:
                old_msg_id = 0
        logger.info(f'[{message["id"]}] {message["username"]}: {message["shout"]}')
        if int(message["id"]) > int(old_msg_id):
            with open("history", "w") as histfile:
                histfile.write(message["id"])
                send_message(
                    context, message["username"], message["shout"], environ["GROUPS"]
                )


updater = Updater(token=environ["BOT_TOKEN"], use_context=True)

job_queue = updater.job_queue
job_queue.run_repeating(tg_shoutbox_monitor, int(environ["MSG_DELAY"]))

updater.start_polling()
updater.idle()
