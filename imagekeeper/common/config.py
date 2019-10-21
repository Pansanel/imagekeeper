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

""" ImageKeeper configuration options.
"""


from oslo_config import cfg
from oslo_log import log

from imagekeeper import version

log.register_options(cfg.CONF)

DEFAULT_OPTS = [
    cfg.StrOpt('cloud_list', default='/etc/imagekeeper/clouds.json',
               help='JSON File containing the configuration options '
                    'required to connect to the cloud backends.'),
    cfg.StrOpt('image_list', default='/etc/imagekeeper/image.list',
               help='File containing the list of images to synchronize over '
                    'the clouds.'),
    cfg.StrOpt('image_format', default='helixnebula',
               help='Format of the image list.'),
    cfg.StrOpt('store_dir', default='/var/lib/imagekeeper',
               help='Directory where the images are downloaded and stored.'),
    cfg.StrOpt('work_dir', default='/var/lib/imagekeeper/tmp',
               help='Work directory where image are downloaded and '
                    'converted.'),
]

cfg.CONF.register_opts(DEFAULT_OPTS)


def parse_args(argv, default_config_files=None):
    """Parse arguments
    """
    cfg.CONF(argv[1:],
             project='imagekeeper',
             version=version.version_info.version_string(),
             default_config_files=default_config_files)


def list_opts():
    """List options
    """
    return [
        ('DEFAULT', DEFAULT_OPTS),
    ]
