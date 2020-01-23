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

"""OpenStack backend class"""

import glanceclient.v2.client as glanceclient
from keystoneauth1 import loading
from keystoneauth1 import session
from oslo_config import cfg
from oslo_log import log

from imagekeeper.backends import base
from imagekeeper.common import utils
from imagekeeper import exception

LOG = log.getLogger(__name__)
CONF = cfg.CONF


class OpenStackBackend(base.Backend):
    """OpenStack backend."""

    def __init__(self, config):
        """Class initialisation.

        :param config: the configuration data
        :type config: dict
        """
        self.config = config

    def _v3oidcaccesstoken_options(self):
        """Return the required options for OIDC auth_type.

        :return: the required options
        :rtype: dict
        """
        required_options = ['auth_url', 'project_name',
                            'project_domain_name', 'oidc_access_token'
                            'oidc_identity_provider', 'oidc_protocol']
        missing_options = utils.validate_options(
            self.config, required_options
        )
        if not missing_options:
            return {
                "auth_url": self.config['auth_url'],
                "project_name": self.config['project_name'],
                "project_domain_name": self.config['project_domain_name'],
                "access_token": self.config['oidc_access_token'],
                "identity_provider": self.config['oidc_identity_provider'],
                "protocol": self.config['oidc_protocol'],
            }
        raise exception.BackendConfigurationMissingOption(
            backend=self.config['backend'],
            auth_type=self.config['auth_type'],
            options=missing_options
        )

    def _v3password_options(self):
        """Return the required options for password auth_type.

        :return: the required options
        :rtype: dict
        """
        required_options = ['auth_url', 'project_name',
                            'project_domain_name', 'oidc_access_token'
                            'oidc_identity_provider', 'oidc_protocol']
        missing_options = utils.validate_options(
            self.config, required_options
        )
        if not missing_options:
            return {
                "auth_url": self.config['auth_url'],
                "project_name": self.config['project_name'],
                "project_domain_name": self.config['project_domain_name'],
                "username": self.config['username'],
                "password": self.config['password'],
                "user_domain_name": self.config['user_domain_name'],
            }
        raise exception.BackendConfigurationMissingOption(
            backend=self.config['backend'],
            auth_type=self.config['auth_type'],
            options=missing_options
        )

    def _auth_options(self, auth_type):
        """Return the options for OpenStack authentificatio.

        :param auth_type: the authenfication type
        :type auth_type: string
        :return: the required options
        :rtype: dict
        """
        LOG.debug("Requesting auth plugin '%s'" % auth_type)
        if auth_type == "v3oidcaccesstoken":
            return self._v3oidcaccesstoken_options()
        if auth_type == "v3password":
            return self._v3password_options()

        raise exception.UnknownAuthMethod(auth_type=auth_type)

    def connect(self):
        """Manage authentification depending the authentication type.

        :return: an OpenStack session
        :rtype: session.Session
        """
        auth_type = self.config['auth_type']
        loader = loading.get_plugin_loader(auth_type)
        auth = loader.load_from_options(**self._auth_options(auth_type))
        return session.Session(auth=auth)

    def get_image_list(self, properties=None):
        """Return the list of images.

        :param properties: a list of properties to use for filtering
        :type properties: dict
        :return: a list of appliances
        :rtype: list
        """
        image_list = {}
        glance = glanceclient.Client(session=self.connect())
        try:
            # TODO: add the ability to filter against private images
            img_generator = glance.images.list()
            image_list = list(img_generator)
        except Exception as err:
            raise exception.UnknownError(err)
        return image_list

    def add_appliance(self, appliance):
        """Add an appliance."""
        glance = glanceclient.Client(session=self.connect())
        LOG.info('Adding appliance: ' + appliance['title'])
        filename = appliance['location']
        image_format = appliance['format']
        image_properties = {}
        min_ram = 0
        if appliance.min_ram:
            min_ram = appliance.min_ram
        if CONF.min_ram > min_ram:
            min_ram = CONF.min_ram
        try:
            image_data = open(filename, 'rb')
        except IOError as err:
            LOG.error("Cannot open image file: '%s'" % filename)
            LOG.exception(err)
            return None

        image_properties['IK_STATUS'] = 'ACTIVE'

        LOG.debug(
            "Creating image '%s' (format: '%s', "
            "properties %s)" % (appliance.title,
                                str.lower(image_format),
                                image_properties)
        )

        glance_image = glance.images.create(
            name=appliance['title'],
            disk_format=str.lower(image_format),
            container_format="bare",
            visibility=CONF.image_visibility,
        )
        glance.images.upload(glance_image.id, image_data)
        glance.images.update(glance_image.id, **image_properties)
        if (min_ram > 0):
            glance.images.update(glance_image.id, min_ram=min_ram)

        image_data.close()

        return glance_image.id
