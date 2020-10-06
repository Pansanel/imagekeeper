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

"""
Loadable plugin support.

This class is used for managing loadable plugins in Imagekeeper. It
is used for detecting and loading image formats and Cloud backends by
loading modules from those directories and find certain types of
classes within those modules. It is based on the OpenStack Nova
plugin module.
"""

import importlib
import inspect
import pkgutil


class PluginLoader(object):
    """Base class for all loadable object."""

    def __init__(self, namespace, loadable_cls_type):
        """Initialize the class."""
        self.namespace = namespace
        self.loadable_cls_type = loadable_cls_type
        self.available_classes = self._get_all_classes()

    def _is_correct_class(self, obj):
        """Check if the class is correct.

        Return whether an object is a class of the correct type and
        is not prefixed with an underscore.
        """
        return (inspect.isclass(obj) and
                (not obj.__name__.startswith('_')) and
                issubclass(obj, self.loadable_cls_type))

    def _get_classes_from_module(self, module_name):
        """Get the classes from a module that match the type we want."""
        classes = []
        module = importlib.import_module(module_name)
        for obj_name in dir(module):
            # Skip objects that are meant to be private.
            if obj_name.startswith('_'):
                continue
            itm = getattr(module, obj_name)
            if self._is_correct_class(itm):
                classes.append(itm)
        return classes

    def _get_all_classes(self):
        """Return the list of classes from modules in a directory.

        Get the classes of the type we want from all modules found
        in the directory that defines this class.
        """
        classes = {}
        module = importlib.import_module(self.namespace)
        for submodule in pkgutil.iter_modules(
                module.__path__, module.__name__ + "."
        ):
            submodule_classes = self._get_classes_from_module(submodule.name)
            for correct_class in submodule_classes:
                classes[correct_class.get_feature()] = correct_class
        return classes

    def load_handler(self, class_type):
        """Load the handler."""
        raise NotImplementedError

    def get_supported_handler(self):
        """Return a list of plugin classes found in this directory."""
        return self.available_classes.keys()
