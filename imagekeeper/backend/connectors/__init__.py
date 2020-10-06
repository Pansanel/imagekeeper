# Copyright 2020 CNRS and University of Strasbourg
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

"""Cloud Connector base class."""

from oslo_config import cfg

from imagekeeper import pluginloader

CONF = cfg.CONF


class BaseConnector(object):
    """Base class for all Cloud connector classes."""

    def __init__(self, feature=None, parameters=None):
        """Initialize the class."""
        self.feature = feature
        if self._verify_parameters():
            self.parameters = parameters

    def _verify_parameters(self):
        """Verify that all required paramters are available."""
        raise NotImplementedError

    def connect(self):
        """Connect to a Cloud."""
        raise NotImplementedError

    def get_feature(self):
        """Return the name of the format."""
        return self.feature


class CloudConnectorHandler(pluginloader.PluginLoader):
    """Base class to handle Cloud connector classe."""

    def __init__(self):
        """Initialize the class."""
        super(CloudConnectorHandler, self).__init__(
            'imagekeeper.backend.connectors', BaseConnector
        )

    def load_handler(self, class_type):
        """Load the connector handler for a Cloud type."""
        connector_handler = None
        connector_classes = self._get_all_classes()
        if class_type in connector_classes.keys():
            connector_handler = connector_classes[class_type]
        return connector_handler
