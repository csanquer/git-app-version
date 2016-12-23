# -*- coding: utf-8 -*-

from mock import patch
import pytest
import subprocess
from git_app_version.helper.process import *

@patch('git_app_version.helper.process.subprocess')
def test_output_command_error(mock_sub_process):
    mock_sub_process.check_output.side_effect = subprocess.CalledProcessError(1, '/bin/false', '')

    assert output_command('/bin/false') == ''
