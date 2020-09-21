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

from imagekeeper.common import exception
from imagekeeper import loadables

CONF = cfg.CONF


class BaseFormat(object):
    """Base class for all format classes."""

    def __init__(self):
        """Initialize the class."""
        pass

    def parse_file(self, filename):
        """Parse an image file."""
        pass


class ImageListFormatHandler(loadables.BaseLoader):
    """Base class to handle loading image format classes.

    This class should be subclassed where one needs to use formats.
    """

    def __init__(self):
        """Initialize the class."""
        super(ImageListFormatHandler, self).__init__(BaseFormat)
        self.format_handler = None

    def _load_format_handler(self):
        """Load the format handler for the image list.

        The get_matching_classes function takes a list as argument and
        return a list. This function verify that only one classe
        matches the format.
        """
        matching_classes = self.get_matching_classes(CONF.image_list_format)
        if len(matching_classes) > 1:
            raise exception.TooManyFormatsFound()
        else:
            self.format_handler = matching_classes[0]()


def all_formats():
    """Return a list of format classes found in this directory.

    This method is used as the default for available image formats
    abd should return a list of all image format available.
    """
    return ImageListFormatHandler().get_all_classes()
