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
    """OpenStack backend
    """
    def __init__(self, config):
        """Class initialisation"""
        self.config = config

    def connect(self):
        """Manage authentification depending the authentication type
        """
        auth_type = self.config['auth_type']
        loader = loading.get_plugin_loader(auth_type)
        auth = loader.load_from_options(**self._auth_options(auth_type))
        return session.Session(auth=auth)

    def _auth_options(self, auth_type):
        LOG.debug("Requesting auth plugin '%s'" % auth_type)
        if auth_type == "v3oidcaccesstoken":
            return self._v3oidcaccesstoken_options()
        if auth_type == "v3password":
            return self._v3password_options()

        raise exception.UnknownAuthMethod(auth_type=auth_type)

    def _v3oidcaccesstoken_options(self):
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

    def get_image_list(self):
        image_list = {}
        glance = glanceclient.Client(session=self.connect())
        try:
            img_generator = glance.images.list()
            image_list = list(img_generator)
        except Exception as err:
            raise.GlanceImageListError(err)
            LOG.error("Not authorized to retrieve the image list from "
                      "the following backend: %s" % self.config['backend_name'])
            LOG.exception(err)
        return image_list


    def add_image(self, image):
        pass

    def depricate_image(self, image_id):
        pass

    def delete_image(self, image_id):
        pass

    def upate_image(self, image):
        pass
