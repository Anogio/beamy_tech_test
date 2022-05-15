from typing import Dict, Tuple

SAMPLE_KEY_MARKER = "sample#"


class InvalidKeyValuePair(Exception):
    pass


def parse_log(log: str) -> Dict[str, str]:
    key_value_pairs = [
        parse_key_value_pair(key_value_pair=key_value_pair)
        for key_value_pair in log.split(" ")
    ]
    return {k: v for k, v in key_value_pairs}


def parse_key_value_pair(key_value_pair: str) -> Tuple[str, str]:
    split_log = key_value_pair.split("=")
    if len(split_log) != 2:
        raise InvalidKeyValuePair
    key, value = split_log[0], split_log[1]
    return format_key(key=key), value


def format_key(key: str) -> str:
    if key.startswith(SAMPLE_KEY_MARKER):
        return key[len(SAMPLE_KEY_MARKER) :]
    return key
