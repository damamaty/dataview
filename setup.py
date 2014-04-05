from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import codecs, os, re, sys, subprocess, imp

try:
    import colorama
    colorama.init()
except ImportError:
    pass

sys.path.append('.')

PACKAGE_NAME = 'dataview'
CODE_DIRECTORY = PACKAGE_NAME
DOCS_DIRECTORY = 'docs'
TESTS_DIRECTORY = 'tests'

test_suite = "unittest2" if sys.version_info < (2,7) else "unittest"

metadata = imp.load_source('metadata', os.path.join(CODE_DIRECTORY, 'metadata.py'))


## Miscellaneous helper functions


def get_project_files():
    """Retrieve a list of project files, ignoring hidden files.

    :return: sorted list of project files
    :rtype: :class:`list`
    """
    if is_git_project():
        return get_git_project_files()

    project_files = []
    for top, subdirs, files in os.walk('.'):
        for subdir in subdirs:
            if subdir.startswith('.'):
                subdirs.remove(subdir)

        for f in files:
            if f.startswith('.'):
                continue
            project_files.append(os.path.join(top, f))

    return project_files

def is_git_project():
    return os.path.isdir('.git')

def get_git_project_files():
    """Retrieve a list of all non-ignored files, including untracked files,
    excluding deleted files.

    :return: sorted list of git project files
    :rtype: :class:`list`
    """
    cached_and_untracked_files = git_ls_files(
        '--cached',  # All files cached in the index
        '--others',  # Untracked files
        # Exclude untracked files that would be excluded by .gitignore, etc.
        '--exclude-standard')
    uncommitted_deleted_files = git_ls_files('--deleted')

    # Since sorting of files in a set is arbitrary, return a sorted list to
    # provide a well-defined order to tools like flake8, etc.
    return sorted(cached_and_untracked_files - uncommitted_deleted_files)

def git_ls_files(*cmd_args):
    """Run ``git ls-files`` in the top-level project directory. Arguments go
    directly to execution call.

    :return: set of file names
    :rtype: :class:`set`
    """
    cmd = ['git', 'ls-files']
    cmd.extend(cmd_args)
    return set(subprocess.check_output(cmd).splitlines())


def print_success_message(message):
    """Print a message indicating success in green color to STDOUT.

    :param message: the message to print
    :type message: :class:`str`
    """
    try:
        import colorama
        print(colorama.Fore.GREEN + message + colorama.Fore.RESET)
    except ImportError:
        print(message)


def print_failure_message(message):
    """Print a message indicating failure in red color to STDERR.

    :param message: the message to print
    :type message: :class:`str`
    """
    try:
        import colorama
        print(colorama.Fore.RED + message + colorama.Fore.RESET, file=sys.stderr)
    except ImportError:
        print(message, file=sys.stderr)

def read(filename):
    """Return the contents of a file.

    :param filename: file path
    :type filename: :class:`str`
    :return: the file's content
    :rtype: :class:`str`
    """
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()

def test():
    """Run the unit tests.

    :return: exit code
    """
    version = sys.version[:3]

    if version == '2.6':
        import unittest2 as unittest
    else:
        import unittest

    loader = unittest.defaultTestLoader
    tests = loader.discover('.')

    return tests

python_version_specific_requires = []


# if sys.version_info < (2, 7) or (3, 0) <= sys.version_info < (3, 3):
#     python_version_specific_requires.append('argparse')
# if sys.version_info < (2, 7):
#     python_version_specific_requires.append('unittest2')


setup_dict = dict(
    name=metadata.package,
    packages = [metadata.package],
    version=metadata.version,
    description=metadata.description,
    long_description=read('README.rst'),
    url=metadata.url,
    author=metadata.authors[0],
    author_email=metadata.emails[0],
    license=metadata.license,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],
    install_requires=[

    ] + python_version_specific_requires,
    zip_safe=False,
    keywords="list slice",
    tests_require=[

    ],
    test_suite=test_suite,
)

def main():
    setup(**setup_dict)

if __name__ == '__main__':
    main()