from common import log_parser


def test_parses_basic_key_value_mapping():
    assert log_parser.parse_log("a_key=my_value") == {"a_key": "my_value"}


def test_parses_multiple_basic_mappings():
    assert log_parser.parse_log("key_1=value_1 key_2=value_2") == {
        "key_1": "value_1",
        "key_2": "value_2",
    }


def test_parses_sample_key_and_keeps_measurement_name():
    assert log_parser.parse_log("normal_key=value sample#some_measurement=1.234") == {
        "normal_key": "value",
        "some_measurement": "1.234",
    }
