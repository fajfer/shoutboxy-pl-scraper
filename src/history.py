HISTORY_FILE_PATH = "history"


def get_latest_id() -> int:
    with open(HISTORY_FILE_PATH) as histfile:
        previous_msg_id = histfile.read().strip()
    return int(previous_msg_id) if previous_msg_id.isnumeric() else 0


def store_latest_id(id: int) -> None:
    with open(HISTORY_FILE_PATH, "w") as histfile:
        histfile.write(str(id))
