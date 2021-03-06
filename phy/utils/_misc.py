# -*- coding: utf-8 -*-

"""Utility functions."""


#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import sys
import os.path as op
from inspect import getargspec

from ..ext.six import string_types, exec_
from ..ext.six.moves import builtins, cPickle


#------------------------------------------------------------------------------
# Pickle utility functions
#------------------------------------------------------------------------------

def _load_pickle(path):
    path = op.realpath(op.expanduser(path))
    assert op.exists(path)
    with open(path, 'rb') as f:
        return cPickle.load(f)


def _save_pickle(path, data):
    path = op.realpath(op.expanduser(path))
    with open(path, 'wb') as f:
        cPickle.dump(data, f, protocol=2)


#------------------------------------------------------------------------------
# Various Python utility functions
#------------------------------------------------------------------------------

def _read_python(path):
    path = op.realpath(op.expanduser(path))
    assert op.exists(path)
    with open(path, 'r') as f:
        contents = f.read()
    metadata = {}
    exec_(contents, {}, metadata)
    metadata = {k.lower(): v for (k, v) in metadata.items()}
    return metadata


def _fun_arg_count(f):
    """Return the number of arguments of a function.

    WARNING: with methods, only works if the first argument is named 'self'.

    """
    args = getargspec(f).args
    if args and args[0] == 'self':
        args = args[1:]
    return len(args)


def _is_in_ipython():
    return '__IPYTHON__' in dir(builtins)


def _is_interactive():
    """Determine whether the user has requested interactive mode."""
    # The Python interpreter sets sys.flags correctly, so use them!
    if sys.flags.interactive:
        return True

    # IPython does not set sys.flags when -i is specified, so first
    # check it if it is already imported.
    if '__IPYTHON__' not in dir(builtins):
        return False

    # Then we check the application singleton and determine based on
    # a variable it sets.
    try:
        from IPython.config.application import Application as App
        return App.initialized() and App.instance().interact
    except (ImportError, AttributeError):
        return False


def _show_shortcut(shortcut):
    if isinstance(shortcut, string_types):
        return shortcut
    elif isinstance(shortcut, tuple):
        return ', '.join(shortcut)


def _show_shortcuts(shortcuts, name=''):
    print()
    if name:
        name = ' for ' + name
    print('Keyboard shortcuts' + name)
    for name in sorted(shortcuts):
        print('{0:<40}: {1:s}'.format(name, _show_shortcut(shortcuts[name])))
    print()
