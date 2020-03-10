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

    def __init__(self, cloud_id, config):
        """Class initialisation.

        :param config: the configuration data
        :type config: dict
        """
        self.cloud_id = cloud_id
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
        glance = glanceclient.Client(session=self.connect())
        try:
            img_generator = glance.images.list()
            image_list = list(img_generator)
        except Exception as err:
            raise exception.UnknownError(err)
        return image_list

    def add_appliance(self, appliance):
        """Add an appliance.

        :param appliance: an appliance to add to Glance
        :type appliance: dict
        :return: True if the appliance could be added successfully
        :rtype: bool
        """
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
            return False

        image_properties['IK_STATUS'] = 'ENABLED'

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

        return True

    def deprecate_appliance(self, appliance_id):
        """Mark an appliance in glance as deprecated.

        :param appliance_id: the id of the appliance
        :type appliance_id: str
        :return: True if the appliance has been successfully marked
        :rtype: bool
        """
        LOG.info("Marking appliance '%s' as deprecated" % appliance_id)
        try:
            glance = glanceclient.Client(session=self.connect())

            glance_images = utils.find_images(glance, appliance_id)
            if not glance_images:
                LOG.error(
                    "Cannot mark image for removal: image '%s' "
                    "not found" % appliance_id
                )
                return False
        except Exception as err:
            LOG.error("Cannot set the appliance '%s' as deprecated "
                      " for the backend '%s'" % (appliance_id, self.cloud_id))
            LOG.exception(err)
            raise exception.UnknownError(err)
        properties = {'IK_STATUS': 'DISABLED'}
        for image in glance_images:
            LOG.debug("Marking image for removal: '%s'" % image.id)
            glance.images.update(image.id, visibility='private', **properties)
        return True

    def delete_appliances(self):
        """Remove all appliances marked as DISABLED.

        :return: True if the cleaning was successfull
        :rtype: bool
        """
        LOG.info("Cleaning up appliances")
        glance = glanceclient.Client(session=self.connect())
        try:
            img_generator = glance.images.list()
            image_list = list(img_generator)
        except Exception as err:
            LOG.error("Could not retrieve the image list for "
                      "the backend '%s'" % self.cloud_id)
            LOG.exception(err)
            return False

        is_deleted = True
        for image in image_list:
            if image.get('IK_STATUS') == 'DISABLED':
                try:
                    LOG.debug("Deleting image '%s'" % image['id'])
                    glance.images.delete(image['id'])
                    LOG.debug(
                        "Image '%s' successfully deleted" % image['id']
                    )
                except Exception as err:
                    LOG.error(
                        "Image '%s' cannot be deleted" % image['id']
                    )
                    LOG.error(err)
                    is_deleted = False
        return is_deleted

    def update_appliance(self, appliance):
        """Update an appliance stored in glance.

        :param appliance:
        :type appliance:
        :return: True if the appliance could be successfully added
        :rtype: bool 
        """
        LOG.info("Updating appliance '%s'" % appliance['id'])
        if not self.deprecate_appliance(appliance['id']):
            LOG.error(
                "Could not mark appliance as deprecated. Appliance will "
                "not be updated"
            )
            return False
        LOG.debug("Old version of the '%s' appliance has been marked for "
                  "removal" % appliance.identifier)
        LOG.debug("Creating new release of the appliance")
        image_id = self.add_appliance(appliance)
        LOG.debug("The glance image '%s' has been created" % image_id)
        return True

    def list_appliance(self, tag_name=None, tag_value=None):
        """List the appliance given a specific tag and value.

        :param tag_name: the name of the tag to filter against
        :type tag_name: str
        :param tag_value: the value of the tag
        :type tag_value: str
        :return: the list of registered appliances
        :rtype: list
        """
        LOG.debug("List appliances having the tag '%s' set with the "
                  "value '%s'" % (tag_name, tag_value))
        image_list = []
        glance = glanceclient.Client(session=self.connect())

        # On some Cloud, the user may not be allowed to list the
        # images. It is required to manage this case.
        try:
            img_generator = glance.images.list()
            image_list = list(img_generator)
        except Exception as err:
            LOG.error("Not authorized to retrieve the image list from "
                      "this cloud: %s" % self.cloud_id)
            LOG.exception(err)
            return image_list
        for image in image_list:
            if image.get(tag_name) == tag_value:
                if image.get('IMAGE_STATUS') == 'DISABLED':
                    LOG.debug("Skipping deprecated image %s" % image['id'])
                else:
                    LOG.debug(
                        "Appending image with id '%s' to the image "
                        "list." % (image['id'])
                    )
                    image_list.append(image['id'])
        return image_list
