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

import os

from imagekeeper.common import exception


class BackendManager(object):
    """A dummy class to manage backends."""

    def __init__(self, cloud_backend_path=None):
        """Initialize the class."""
        self.backends = {}
        if cloud_backend_path:
            if not os.path.isfile(cloud_backend_path):
                raise exception.BackendFileNotFound(
                    cloud_backend_file=cloud_backend_path,
                )

            # parse config file
            self._parse_config_file(cloud_backend_path)

    def get_backends(self):
        """Return the backend list."""
        return self.backends

    def _parse_config_file(self, cloud_backend_path):
        """Parse the backend configuration file."""
        # TODO: Write the parsing function
        pass
