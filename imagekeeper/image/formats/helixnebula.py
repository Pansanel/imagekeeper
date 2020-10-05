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

"""Plugin for Helix Nebula based image list format."""

from imagekeeper.image import formats


class HelixNebula(formats.BaseFormat):
    """HelixNebula Format class."""

    def __init__(self):
        """Initialize the class."""
        super(HelixNebula, self).__init__('helixnebula')

    def parse_file(self, filename):
        """Parse an image file."""
        pass
