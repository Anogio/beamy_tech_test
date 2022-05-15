import pytest
import shutil
import os

from level_1 import constants, level_1_app


@pytest.fixture
def clean_up_parsed_folder():
    if os.path.exists(constants.PARSED_FOLDER_PATH) and os.path.isdir(
        constants.PARSED_FOLDER_PATH
    ):
        shutil.rmtree(constants.PARSED_FOLDER_PATH)


@pytest.fixture
def level_1_client(clean_up_parsed_folder):
    app = level_1_app.create_app()
    app.debug = True
    return app.test_client()
