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

"""ImageKeeper exception subclasses"""

import sys

from oslo_config import cfg
from oslo_log import log

import six

LOG = log.getLogger(__name__)
CONF = cfg.CONF


class ImageKeeperException(Exception):
    """Base ImageKeeper Exception

    To correctly use this class, inherit from it and define a 'message'
    property. That message will get printf'd with the keyboard arguments
    provided to the constructor.
    """
    msg_fmt = "An unknown exception occurred."

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if not message:
            try:
                message = self.msg_fmt % kwargs
            except Exception:
                exc_info = sys.exc_info()
                # kwargs doesn't match a variable in the message
                # log the issue and the kwargs
                LOG.exception('Exception in string format operation for'
                              '%s exception', self.__class__.__name__)
                for name, value in kwargs.items():
                    LOG.error("%s: %s" % (name, value))

                six.reraise(exc_info[0], exc_info[1], exc_info[2])

        super(ImageKeeperException, self).__init__(message)


class FunctionNotImplemented(ImageKeeperException):
    """Exception raised when a function is not implemented.
    """
    msg_format = "The function you have requested has not been implemented."


class BackendNotFound(ImageKeeperException):
    """Exception raised when a backend is not found.
    """
    msg_fmt = "Backend %(backend) could not be found: %(exception)s."


class BadBackendConfiguration(ImageKeeperException):
    """Exception raised when the backend cannot be configured.
    """
    msg_fmt = "Backend %(backend) could not be configured: %(exception)s."
