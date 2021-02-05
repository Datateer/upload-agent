import os 
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner
import pytest

from datateer.upload_agent.main import cli
from datateer.upload_agent.config import save_config
import datateer.upload_agent.constants as constants


@pytest.fixture
def runner():
    return CliRunner()


def test_command_config_upload_agent_handles_show_flag(runner):
    result = runner.invoke(cli, ['config', 'upload-agent', '--show'])
    assert result.exit_code == 0


def test_command_config_feed_handles_show_flag(runner):
    result = runner.invoke(cli, ['config', 'feed', '--show'])
    assert result.exit_code == 0


def test_command_upload_handles_feed_key_and_path_arguments(runner):
    result = runner.invoke(cli, ['upload', 'FEED-KEY', 'PATH'])
    assert result.exit_code == 0


def test_command_upload_handles_individual_file_argument(runner):
    result = runner.invoke(cli, ['upload', 'FEED-KEY', 'PATH.csv'])
    assert result.exit_code == 0


def test_command_upload_handles_directory_argument(runner):
    result = runner.invoke(cli, ['upload', 'FEED-KEY', 'PATH/'])
    assert result.exit_code == 0



@patch.dict('datateer.upload_agent.main.config', constants.SAMPLE_CONFIG, clear=True)
def test_config_upload_agent_prompts_show_defaults_if_config_exists(runner, config):
    defaults = config

    result = runner.invoke(cli, ['config', 'upload-agent'], input='CLIENT-CODE\nRAW-BUCKET\nACCESS-KEY\nACCESS-SECRET')
    
    print(result.output)
    assert result.exit_code == 0
    assert f'Client code [{defaults["client-code"]}]: CLIENT-CODE' in result.output
    assert f'Raw bucket name [{defaults["upload-agent"]["raw-bucket"]}]: RAW-BUCKET' in result.output
    assert f'Access key [{defaults["upload-agent"]["access-key"]}]: ACCESS-KEY' in result.output
    assert f'Access secret [{defaults["upload-agent"]["access-secret"]}]: ACCESS-SECRET' in result.output

@patch.dict('datateer.upload_agent.main.config', {'client-code': 'TEST-CLIENT-CODE'}, clear=True)
def test_config_feed_prompts(runner):
    result = runner.invoke(cli, ['config', 'feed'], input='PROVIDER\nSOURCE\nFEED\nFEED-KEY')
    assert result.exit_code == 0
    assert 'Provider [TEST-CLIENT-CODE]: PROVIDER' in result.output
    assert 'Source: SOURCE' in result.output
    assert 'Feed: FEED' in result.output
    assert 'Feed key [FEED]: FEED-KEY' in result.output


@patch.dict('datateer.upload_agent.main.config', {'client-code': 'MY-TEST-CLIENT-CODE'})
def test_config_feed_provider_code_defaults_to_client_code(runner):
    client_code = 'MY-TEST-CLIENT-CODE'
    result = runner.invoke(cli, ['config', 'feed', '--source', 'SOURCE', '--feed', 'FEED'], input='\n\n')
    assert f'Provider [{client_code}]:' in result.output
    assert f'Provider [{client_code}]: {client_code}' not in result.output # assert user did not type in a value

def test_config_feed_key_defaults_to_feed_code(runner):
    result = runner.invoke(cli, ['config', 'feed', '--provider', 'PROVIDER', '--source', 'SOURCE', '--feed', 'FEED'])
    assert 'Feed key [FEED]:' in result.output
    assert 'Feed key [FEED]: FEED' not in result.output # user did not type in a value

def test_show_version(runner):
    pytest.skip()

