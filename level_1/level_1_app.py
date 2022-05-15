from flask import Flask
from flask import request
from flask import abort
import os
import json

from level_1 import constants
from common import log_parser
from common.log_parser import InvalidKeyValuePair


def create_app():
    app = Flask(__name__)

    if not os.path.exists(constants.PARSED_FOLDER_PATH):
        os.mkdir(constants.PARSED_FOLDER_PATH)

    @app.route("/", methods=["POST"])
    def parse_log():
        log_line = request.get_json()["log"]
        try:
            parsed_log_line = log_parser.parse_log(log_line)

            with open(
                os.path.join(
                    constants.PARSED_FOLDER_PATH, f"#{parsed_log_line['id']}.json"
                ),
                "w",
            ) as f:
                json.dump(parsed_log_line, f)
        except InvalidKeyValuePair:
            abort(400)

        return "Success"

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=3000)
