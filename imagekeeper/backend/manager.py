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

import json
import os

from oslo_config import cfg

from imagekeeper.common import exception
from imagekeeper.backend import connectors

CONF = cfg.CONF


class BackendManager(object):
    """A class for managing Cloud backends."""

    def __init__(self):
        """Initialize the class."""
        self.backends = {}
        self.schema = {
            'name': str,
            'type': str,
            'parameters': dict
        }
        if not os.path.isfile(CONF.cloud_backend_path):
            raise exception.BackendFileNotFound(
                cloud_backend_file=CONF.cloud_backend_path,
            )

        # parse config file
        self._parse_config_file(CONF.cloud_backend_path)
        self.backend_handler = connectors.CloudConnectorHandler()

    def get_backends(self):
        """Return the backend list."""
        return self.backends

    def _parse_config_file(self, cloud_backend_path):
        """Parse the backend configuration file."""
        config_file = open(cloud_backend_path, 'r')
        backend_configs = json.load(config_file)
        if not self._validate(backend_configs):
            raise exception.InvalidBackendFile(
                cloud_backend_file=CONF.cloud_backend_path,
            )
        for backend in backend_configs:
            handler = self.backend_handler.load_handler(
                backend['type']
            )
            self.backends[backend['name']] = handler(
                parameters=backend['parameters']
            )

    def _validate(self, json_data):
        """Validate the structure of the JSON configuration file."""
        name_list = []
        for backend in json_data:
            if set(backend) != set(self.schema):
                return False
            for key in self.schema:
                if not isinstance(backend[key], self.schema[key]):
                    return False
            if backend['name'] in name_list:
                return False
            name_list.append(backend['name'])
        return True
