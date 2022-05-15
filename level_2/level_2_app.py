from flask import Flask
from flask import request

from level_2 import constants, computation_worker
from level_2.config import redis_client


def create_app():
    app = Flask(__name__)

    @app.route("/", methods=["POST"])
    def parse_log():
        log_line = request.get_json()["log"]
        redis_client.lpush(constants.REDIS_WIP_LIST, log_line)
        return "Success"

    return app


if __name__ == "__main__":
    computation_worker.start_worker()
    create_app().run(host="0.0.0.0", port=3000)
