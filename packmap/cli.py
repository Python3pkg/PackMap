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
import argparse
import subprocess
import json

from packmap import env
from packmap import finder


class PackMapClient(object):

    def __init__(self):
        self.args = None
        self.parser = self.build_arguments(argparse.ArgumentParser())
        self._finder_path = finder.__file__
        self.results = {}

    def parse_args(self):
        self.args = self.parser.parse_args()

        if 'path' in self.args.install_type and not self.args.install_path:
            print('You must specify --install-path when using the "path" '
                  'install type')
            exit(1)

        return self.args

    def build_arguments(self, parser):
        # Required Args
        parser.add_argument('package_name', type=str)

        # Options
        parser.add_argument('--install-type', type=str, default='pypi')
        parser.add_argument('--install-path', type=str)
        parser.add_argument('--keep-env', action='store_true')
        parser.add_argument('--no-json-results', action='store_true')

        return parser

    def execute_finder(self, manager, package_name):
        """ Execute finder script within the temporary venv context. """
        filename = '{env_path}/results.json'.format(env_path=manager.env_path)
        subprocess.call([
            manager.venv_python, self._finder_path, package_name, filename
        ])

        # Load results into this context
        json_str = open(filename, 'r').read()
        return json.loads(json_str)

    def write_results_to_file(self, results, filename):
        json_file = open(filename, 'w')
        json_file.write(json.dumps(results))

    def run(self):
        args = self.parse_args()

        manager = env.EnvironmentManager()
        manager.build()

        # Install package
        print('Installing package into environment...')
        install_name = args.package_name
        if 'path' in args.install_type:
            install_name = args.install_path

        manager.install_package(install_name)

        # Find Requirements
        self.results = self.execute_finder(manager, args.package_name)

        if not args.no_json_results:
            filename = './{pkg_name}.json'.format(pkg_name=args.package_name)
            self.write_results_to_file(self.results, filename)

        if not args.keep_env:
            manager.clean_up()


def main(*args, **kwargs):
    client = PackMapClient()
    client.run()

if __name__ == '__main__':
    main()
