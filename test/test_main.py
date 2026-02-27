# Copyright 2021 Ruffin White
# Licensed under the Apache License, Version 2.0

import argparse
import subprocess
import os
from pathlib import Path
import shutil
import sys
from tempfile import mkdtemp

from colcon_core.command import main
import pytest


def _raising_error(self, message):
    raise sys.exc_info()[1]


argparse.ArgumentParser.error = _raising_error


def test_main(monkeypatch):
    """System test for colcon direnv CLI."""
    ws_base = Path(mkdtemp(prefix='test_colcon_'))
    resources_base = Path('test', 'resources').absolute()
    shutil.copytree(resources_base / 'ws/src', ws_base / 'src')


    os.chdir(ws_base)

    os.environ['COLCON_EXTENSION_BLOCKLIST'] = (
        'colcon_core.event_handler.desktop_notification:' +
        os.environ.get('COLCON_EXTENSION_BLOCKLIST', ''))

    main(argv=['direnv'])

    # Assert the .envrc and defaults.json file exists
    assert (ws_base / 'defaults.json').exists()
    assert (ws_base / '.envrc').exists()

    subprocess.check_call(['direnv', 'allow'], cwd=ws_base)

    subprocess.check_call(
        ['direnv', 'exec', str(ws_base),
         'colcon', 'build',
         '--packages-select', 'test_py_pkg'],
        cwd=ws_base / 'src')

    assert (ws_base / 'build').exists()
    assert (ws_base / 'install').exists()
