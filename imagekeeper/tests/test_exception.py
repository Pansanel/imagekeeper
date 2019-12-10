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

"""OpenStack backend test class
"""

import six

from imagekeeper import exception
from imagekeeper.tests import base


class TestImageKeeperException(base.TestCase):
    """Test ImageKeeper Exception
    """
    def test_default_error_msg(self):
        """Test the error class with a fake exception
        """
        class FakeImagekeeperException(exception.ImagekeeperException):
            """A fake exception class
            """
            message = "default message"

        exc = FakeImagekeeperException()
        self.assertEqualt('default message', six.text_type(exc))
