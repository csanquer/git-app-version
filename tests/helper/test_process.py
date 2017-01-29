# -*- coding: utf-8 -*-

import subprocess

import pytest
from mock import patch

from git_app_version.helper.process import *


@patch('git_app_version.helper.process.subprocess')
def test_output_command_error(mock_sub_process):
    mock_sub_process.check_output.side_effect = subprocess.CalledProcessError(
        1, '/bin/false', '')

    assert output_command('/bin/false') == ''
