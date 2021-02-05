import os
from pathlib import Path
import pytest

import datateer.upload_agent.constants as constants
from datateer.upload_agent.config import save_config

@pytest.fixture
def config_path(tmp_path):
    from datateer.upload_agent.config import DEFAULT_PATH
    path = Path(tmp_path / DEFAULT_PATH)
    path.resolve().parent.mkdir(parents=True, exist_ok=True)
    return path

@pytest.fixture
def sample_config_dict():
    return constants.SAMPLE_CONFIG

@pytest.fixture
def config(config_path, sample_config_dict):
    os.chdir(config_path.resolve().parent)
    return save_config(sample_config_dict)
