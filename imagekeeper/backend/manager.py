# Copyright 2019 CNRS and University of Strasbourg
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Class for managing backends."""


class BackendManager(object):
    """A dummy class to manage backends."""

    def __init__(self, config_file=None):
        """Initialize the class."""
        self.backends = {}
        if config_file:
            # parse config file
            self._parse_config_file(config_file)

    def get_backends(self):
        """Return the backend list."""
        return self.backends

    def _parse_config_file(self, config_file):
        """Parse the backend configuration file."""
        # TODO: Write the parsing function
        pass
