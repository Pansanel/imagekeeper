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

from oslo_config import cfg

from imagekeeper.common import exception
from imagekeeper.image import formats

CONF = cfg.CONF


class ImageListManager(object):
    """A dummy class to manage backends."""

    def __init__(self):
        """Initialize the class."""
        if not os.path.isfile(CONF.image_list_path):
            raise exception.ImageListFileNotFound(
                image_list_file=CONF.image_list_path
            )
        self.images = {}
        self.format_cls_map = {}
        self.format_handler = formats.ImageListFormatHandler()
        classes = self.format_handler.get_matching_classes(
            CONF.image_list_format
        )
        if len(classes) == 1:
            self.format_obj = classes[0]()

    def get_images(self):
        """Return the backend list."""
        return self.images
