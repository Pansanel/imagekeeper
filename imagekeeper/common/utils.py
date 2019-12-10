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

"""A set of utils for ImageKeeper
"""

import math


def convert_ram(ram_value):
    """Convert ram in bytes to the nearest upper integer in megabytes
    """
    return int(math.ceil(ram_value/1048576))


def validate_options(config, options):
    """Return the list of missing options
    """
    missing_options = []
    for option in options:
        if option not in config:
            missing_options.append(option)
    return missing_options
