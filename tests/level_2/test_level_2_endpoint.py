import json
import time
from level_2 import constants


def test_endpoint_with_simple_log_respects_timeout(level_2_client, redis_client):
    t0 = time.perf_counter()  # The Flask test client does not support timeout
    response = level_2_client.post("/", json={"log": "id=my_id key=value"})
    t = time.perf_counter()

    assert response.status_code == 200
    assert t - t0 <= 0.1

    time.sleep(5)
    assert redis_client.llen(constants.REDIS_PROCESSED_LOGS_LIST) == 1
    assert json.loads(redis_client.lpop(constants.REDIS_PROCESSED_LOGS_LIST)) == {
        "id": "my_id",
        "key": "value",
        "slow_computation": "0.0009878",
    }


def test_endpoint_with_multiple_logs_respects_fifo_order(level_2_client, redis_client):
    # Here we assume that the end of the queue is on the right
    response = level_2_client.post("/", json={"log": "id=my_id key=value"})
    assert response.status_code == 200

    response = level_2_client.post("/", json={"log": "id=my_id_2 key=value_2"})
    assert response.status_code == 200

    time.sleep(7)  # TODO: mock out the computation to speed up the tests
    assert redis_client.llen(constants.REDIS_PROCESSED_LOGS_LIST) == 2
    assert json.loads(redis_client.rpop(constants.REDIS_PROCESSED_LOGS_LIST)) == {
        "id": "my_id",
        "key": "value",
        "slow_computation": "0.0009878",
    }

    assert json.loads(redis_client.rpop(constants.REDIS_PROCESSED_LOGS_LIST)) == {
        "id": "my_id_2",
        "key": "value_2",
        "slow_computation": "0.0009878",
    }
