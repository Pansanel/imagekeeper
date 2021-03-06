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

"""Image list format base class."""

from oslo_config import cfg

from imagekeeper import pluginloader

CONF = cfg.CONF


class BaseFormat(object):
    """Base class for all format classes."""

    def __init__(self, feature=None):
        """Initialize the class."""
        self.feature = feature

    def parse_file(self, filename):
        """Parse an image file."""
        raise NotImplementedError

    def get_feature(self):
        """Return the name of the format."""
        return self.feature


class ImageListFormatHandler(pluginloader.PluginLoader):
    """Base class to handle loading image format classes."""

    def __init__(self):
        """Initialize the class."""
        super(ImageListFormatHandler, self).__init__(
            'imagekeeper.image.formats', BaseFormat
        )

    def load_handler(self, class_type):
        """Load the format handler for the image list."""
        format_handler = None
        format_classes = self._get_all_classes()
        if class_type in format_classes.keys():
            format_handler = format_classes[class_type]
        return format_handler
