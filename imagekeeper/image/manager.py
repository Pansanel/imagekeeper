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

"""Class for managing an image list."""

import os

from oslo_config import cfg

from imagekeeper.common import exception
from imagekeeper.image import formats

CONF = cfg.CONF


class ImageListManager(object):
    """A class for managing an image list."""

    def __init__(self):
        """Initialize the class."""
        if not os.path.isfile(CONF.image_list_path):
            raise exception.ImageListFileNotFound(
                image_list_file=CONF.image_list_path
            )
        self.images = {}
        self.format_cls_map = {}
        self.format_handler = formats.ImageListFormatHandler()

    def _parse_image_list(self):
        """Parse the image list."""
        image_list_handler = self.format_handler.load_handler(
            CONF.image_list_format
        )
        return image_list_handler

    def get_images(self):
        """Return the backend list."""
        return self.images
