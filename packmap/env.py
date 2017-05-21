"""
Copyright 2014 John Vrbanac

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import uuid
import virtualenv as venv
import shutil
import subprocess


class EnvironmentManager(object):

    def __init__(self):
        self._uuid = uuid.uuid4()
        self._install_type = 'pypi'
        self._package_name = ''
        self._env_path = '/tmp/packmap/{uuid}'.format(uuid=self._uuid)
        self._python = 'python'

    def build(self):
        print(('Building Python Virtual Environment: {0}...'.format(self.uuid)))
        home_dir, lib_dir, inc_dir, bin_dir = venv.path_locations(
            self._env_path)

        self._python = os.path.abspath(venv.install_python(
            home_dir, lib_dir, inc_dir, bin_dir, site_packages=False,
            clear=False, symlink=True))

        venv.install_wheel(['setuptools', 'pip'], self._python, None)
        venv.install_distutils(home_dir)

        print('Build complete!')
        return self._python

    def clean_up(self):
        print(('Deleting environment: {uuid}'.format(uuid=self._uuid)))
        shutil.rmtree(self._env_path, ignore_errors=True)

    def install_package(self, package_name):
        pip = '{env_path}/bin/pip'.format(env_path=self._env_path)
        subprocess.call([pip, 'install', package_name])

    @property
    def venv_python(self):
        return self._python

    @property
    def env_path(self):
        return self._env_path

    @property
    def uuid(self):
        return self._uuid
