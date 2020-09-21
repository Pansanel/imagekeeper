#!/usr/bin/env python3
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
from imagekeeper.backend import manager as backend_manager
from imagekeeper.image import manager as image_manager

CONF = cfg.CONF
LOG = log.getLogger(__name__)


def main():
    """Imagekeeper main script."""
    config.parse_args(sys.argv)
    log.setup(CONF, 'imagekeeper')

    LOG.info('Starting imagekeeper')

    # Read the content of the image list
    images = image_manager.ImageListManager()
    if not images:
        raise exception.NoImageFound(
            image_list=CONF.image_list_path,
        )

    # Read the content of the cloud backend configuration file
    backends = backend_manager.BackendManager()
    if not backends:
        raise exception.NoBackendDefined(
            cloud_config=CONF.cloud_backend_file,
        )

    for backend in backends.get_backends():
        LOG.info("Managing images at %s" % backend['name'])
        for image in images.get_images():
            LOG.info(image)


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        sys.stderr.write(err.__str__())
        sys.exit(1)
