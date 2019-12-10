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

"""Default backend class"""

import abc
import six

from oslo_config import cfg
from oslo_log import log

from imagekeeper import exception

LOG = log.getLogger(__name__)
CONF = cfg.CONF


@six.add_metaclass(abc.ABCMeta)
class Backend(object):
    """ImageKeeper AbException

    To correctly use this class, inherit from it and define a 'message'
    property. That message will get printf'd with the keyboard arguments
    provided to the constructor.
    """
    @abc.abstractmethod
    def connect(self):
        """Connect to the backend"""
        raise exception.FunctionNotImplemented()

    @abc.abstractmethod
    def get_image_list(self, **kwargs):
        """Retrieve the image list from the backend
        """
        raise exception.FunctionNotImplemented()

    @abc.abstractmethod
    def add_image(self, **kwargs):
        """Add an image
        """
        raise exception.FunctionNotImplemented()

    @abc.abstractmethod
    def depricate_image(self, **kwargs):
        """Set a image as depricated
        """
        raise exception.FunctionNotImplemented()

    @abc.abstractmethod
    def delete_image(self, **kwargs):
        """Try to delete depricated images
        """
        raise exception.FunctionNotImplemented()

    @abc.abstractmethod
    def update_image(self, **kwargs):
        """Update an image
        """
        raise exception.FunctionNotImplemented()
