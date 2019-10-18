#!/usr/bin/env python
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

"""Starter script for ImageKeeper."""

import sys

from oslo_config import cfg
from oslo_log import log

from imagekeeper.common import config
from imagekeeper.common import exception

CONF = cfg.CONF
LOG = log.getLogger(__name__)

KNOWN_EXCEPTIONS = (RuntimeError,
                    exception.BadBackendConfiguration,
                    ValueError)


def fail(e):
    global KNOWN_EXCEPTIONS
    return_code = KNOWN_EXCEPTIONS.index(type(e)) + 1
    sys.stderr.write("ERROR: %s\n" % e)
    sys.exit(return_code)


def main():
    """ImageKeeper main script
    """
    try:
        config.parse_args()
        config.set_config_defaults()
        log.setup(CONF, 'imagekeeper')

        LOG.info('Starting imagekeeper')
    except KNOWN_EXCEPTIONS as e:
        fail(e)


if __name__ == "__main__":
    main()
