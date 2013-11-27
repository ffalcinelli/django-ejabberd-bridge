#!/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2013  Fabio Falcinelli
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from setuptools import find_packages, setup, Command
import sys

__author__ = 'fabio'


class RunTests(Command):
    description = 'Run the django test suite from the tests dir.'
    user_options = []
    extra_env = {}
    extra_args = []

    def run(self):
        for env_name, env_value in self.extra_env.items():
            os.environ[env_name] = str(env_value)

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")

        from django.core.management import execute_from_command_line

        execute_from_command_line(sys.argv)

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


setup(name='django-ejabberd-bridge',
      version='0.0.1',
      description='A django app for ejabberd external authentication',
      author='Fabio Falcinelli',
      author_email='fabio.falcinelli@gmail.com',
      url='https://github.com/ffalcinelli/django-ejabberd-bridge',
      keywords=['django', 'ejabberd', 'authentication'],
      packages=find_packages(),
      license="LGPLv3",
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Intended Audience :: Telecommunications Industry',
          'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Utilities',
          'Topic :: Software Development :: Libraries :: Application Frameworks',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      install_requires=[
          'django',
          'mock'],
      cmdclass={"test": RunTests}
)