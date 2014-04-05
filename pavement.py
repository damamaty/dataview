# -*- coding: utf-8; -*-

from __future__ import print_function

import os, sys, time, subprocess
from paver.easy import options, task, needs, consume_args

sys.path.append('.')

import setup
from setup import test, print_failure_message, print_success_message

if sys.version_info < (2,7):
    import unittest2 as unittest
else:
    import unittest

## Miscellaneous helper functions

def print_passed():
    print_success_message(r''' ___  _   ___ ___ ___ ___
| _ \/_\ / __/ __| __|   \
|  _/ _ \\__ \__ \ _|| |) |
|_|/_/ \_\___/___/___|___/
    ''')


def print_failed():
    print_failure_message(r''' ___ _   ___ _    ___ ___
| __/_\ |_ _| |  | __|   \
| _/ _ \ | || |__| _|| |) |
|_/_/ \_\___|____|___|___/
    ''')


## Task-related functions

def _doc_make(*make_args):
    """Run make in sphinx' docs directory.

    :return: exit code
    """
    if sys.platform == 'win32':
        # Windows
        make_cmd = ['make.bat']
    else:
        # Linux, Mac OS X, and others
        make_cmd = ['make']
    make_cmd.extend(make_args)

    return subprocess.call(make_cmd, cwd=setup.DOCS_DIRECTORY)

## Tasks

@task
def test():
    """Run the unit tests."""
    retcode = unittest.TextTestRunner().run(setup.test())

    if len(retcode.failures) == 0:
        print_passed()
    else:
        print_failed()

    raise SystemExit()

@task
def doc_html():
    """Build the HTML docs."""
    retcode = _doc_make('html')

    if retcode:
        raise SystemExit(retcode)


@task
def doc_clean():
    """Clean (delete) the built docs."""
    retcode = _doc_make('clean')

    if retcode:
        raise SystemExit(retcode)

@task
@needs('doc_html')
def doc_open():
    """Build the HTML docs and open them in a web browser."""
    doc_index = os.path.join(setup.DOCS_DIRECTORY, 'build', 'html', 'index.html')
    if sys.platform == 'darwin':
        # Mac OS X
        subprocess.check_call(['open', doc_index])
    elif sys.platform == 'win32':
        # Windows
        subprocess.check_call(['start', doc_index], shell=True)
    elif sys.platform == 'linux2':
        # All freedesktop-compatible desktops
        subprocess.check_call(['xdg-open', doc_index])
    else:
        print_failure_message("Unsupported platform. Please open `{0}' manually.".format(doc_index))

@task  # NOQA
def doc_watch():
    """Watch for changes in the docs and rebuild HTML docs when changed."""
    try:
        from watchdog.events import FileSystemEventHandler
        from watchdog.observers import Observer
    except ImportError:
        print_failure_message('Install the watchdog package to use this task, '
                              "i.e., `pip install watchdog'.")
        raise SystemExit(1)

    class RebuildDocsEventHandler(FileSystemEventHandler):
        def __init__(self, base_paths):
            self.base_paths = base_paths

        def dispatch(self, event):
            """Dispatches events to the appropriate methods.
            :param event: The event object representing the file system event.
            :type event: :class:`watchdog.events.FileSystemEvent`
            """
            for base_path in self.base_paths:
                if event.src_path.endswith(base_path):
                    super(RebuildDocsEventHandler, self).dispatch(event)
                    # We found one that matches. We're done.
                    return

        def on_modified(self, event):
            print_failure_message('Modification detected. Rebuilding docs.')
            # # Strip off the path prefix.
            # import os
            # if event.src_path[len(os.getcwd()) + 1:].startswith(
            #         CODE_DIRECTORY):
            #     # sphinx-build doesn't always pick up changes on code files,
            #     # even though they are used to generate the documentation. As
            #     # a workaround, just clean before building.
            doc_html()
            print_success_message('Docs have been rebuilt.')

    print_success_message(
        'Watching for changes in project files, press Ctrl-C to cancel...')
    handler = RebuildDocsEventHandler(get_project_files())
    observer = Observer()
    observer.schedule(handler, path='.', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()