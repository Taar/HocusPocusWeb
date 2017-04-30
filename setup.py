#!/usr/bin/env python

import sys

from setuptools.command.test import test as TestCommand
from setuptools import setup, find_packages


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['-s']

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


install_requires = [
    'setuptools',
    'pyramid',
    'pyramid_jinja2',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'wtforms',
    'gunicorn',
]

tests_require = [
    'pytest',
    'mock',
]

setup_requires = [
    'pytest-runner',
]

setup(
    name='HocusPocusWeb',
    version='0.1',
    description='Authentication portal',
    author='Randy Topliffe',
    author_email='randytopliffe@gamil.com',
    url='https://github.com/Taar/HocusPocusWeb',
    packages=find_packages(),
    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_require,
    cmdclass={'test': PyTest},
    test_suite="tests",
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Programming Language :: Python',
        "Framework :: Pyramid",
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    entry_points="""\
    [paste.app_factory]
    main = hocuspocusweb:main
    [console_scripts]
    initialize_HocusPocusweb_db = hocuspocusweb.scripts.initializedb:main
    """,
    zip_safe=False,
    include_package_data=True,
)
