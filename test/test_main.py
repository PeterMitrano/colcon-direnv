# Copyright 2021 Ruffin White
# Licensed under the Apache License, Version 2.0

import argparse
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
    ws_base.mkdir('src')

    os.chdir(ws_base)

    os.environ['COLCON_EXTENSION_BLOCKLIST'] = (
        'colcon_core.event_handler.desktop_notification:' +
        os.environ.get('COLCON_EXTENSION_BLOCKLIST', ''))

    main(argv=['direnv'])

    # Assert the defaults.json file exists
    assert (ws_base / '.defaults.json').exists()
    # Assert .envrc does NOT exist
    assert not (ws_base / '.envrc').exists()

    main(argv=['build'])

    # Now check that the correct build and install paths exist
    assert (ws_base / 'build').exists()
    assert (ws_base / 'install').exists()
