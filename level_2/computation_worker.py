import json
import time

from common import log_parser
from level_2 import slow_computation, constants
from level_2.config import redis_client

from threading import Thread
import logging

logger = logging.getLogger()  # TODO: use logging instead of print


def process_one_log(log_line: str) -> dict:
    parsed_log_line = log_parser.parse_log(log=log_line)
    return slow_computation.compute(payload=parsed_log_line)


def get_and_process_one_log() -> None:
    if redis_client.llen(constants.REDIS_WIP_LIST) > 0:
        log_line = redis_client.rpop(constants.REDIS_WIP_LIST).decode()
        print(f"Processing line {log_line}")
        processed_log_line = process_one_log(log_line)
        redis_client.lpush(
            constants.REDIS_PROCESSED_LOGS_LIST, json.dumps(processed_log_line)
        )


def worker_main_loop():
    while True:
        try:
            get_and_process_one_log()
            time.sleep(0.1)
        except Exception as e:
            # The worker should not crash if it fails to process a log
            print(f"Could not process log line: {e}")


def start_worker():
    print("Starting worker")
    worker_thread = Thread(target=worker_main_loop)
    worker_thread.start()
