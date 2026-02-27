# Copyright 2021 Ruffin White
# Licensed under the Apache License, Version 2.0

from unittest.mock import Mock

from colcon_direnv.verb.direnv import direnvVerb
from colcon_core.command import CommandContext


class Object(object):
    pass


def test_verb_interface():
    interface = direnvVerb()
    interface._subparser = Object()
    interface._subparser.format_usage = Mock(return_value='')

    args = Object()
    context = CommandContext(command_name='direnv', args=args)

    rc = interface.main(context=context)
    assert rc is None
