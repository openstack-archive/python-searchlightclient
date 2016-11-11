#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from searchlightclient.common import base


class ResourceType(base.Resource):
    def __repr__(self):
        return "<ResourceType %s>" % self._info

    def list(self, **kwargs):
        return self.manager.list(self, **kwargs)


class ResourceTypeManager(base.BaseManager):
    resource_class = ResourceType

    def list(self, **kwargs):
        """Get a list of plugins.
        :rtype: list of :class:`ResourceType`
        """
        return self._list('/v1/search/plugins', 'plugins')
