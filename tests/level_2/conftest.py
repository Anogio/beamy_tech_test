import pytest
import redis

from level_2 import level_2_app, constants, computation_worker


def pytest_configure(config):
    # TODO: use a signal to kill the worker
    computation_worker.start_worker()


@pytest.fixture
def redis_client():
    return redis.Redis(host="localhost", port=6379)


@pytest.fixture
def clean_redis_list(redis_client):
    while redis_client.llen(constants.REDIS_PROCESSED_LOGS_LIST) != 0:
        redis_client.lpop(constants.REDIS_PROCESSED_LOGS_LIST)
    while redis_client.llen(constants.REDIS_WIP_LIST) != 0:
        redis_client.lpop(constants.REDIS_WIP_LIST)


@pytest.fixture
def level_2_client(clean_redis_list):
    app = level_2_app.create_app()
    app.debug = True
    return app.test_client()
