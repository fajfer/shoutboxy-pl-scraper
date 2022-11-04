HISTORY_FILE_PATH = "history"


def get_latest_id() -> int:
    with open(HISTORY_FILE_PATH) as history_file:
        previous_msg_id = history_file.read().strip()
    return int(previous_msg_id) if previous_msg_id.isnumeric() else 0


def store_latest_id(id: int) -> None:
    with open(HISTORY_FILE_PATH, "w") as history_file:
        history_file.write(str(id))
