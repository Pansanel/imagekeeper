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

from imagekeeper.backend import openstack
from imagekeeper.tests import base


class TestOpenStackBackend(base.TestCase):
    """Test OpenStack backend
    """
    def test_convert_ram(self):
        """Test the conver_ram function
        """
        self.assertEqual(1, utils.convert_ram(1048576))
