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

from searchlightclient.v1 import resource_types

import testtools
from unittest import mock


class ResourceTypeManagerTest(testtools.TestCase):

    def test_list(self):
        manager = resource_types.ResourceTypeManager(None)
        manager._list = mock.Mock()
        manager.list()
        manager._list.assert_called_once_with('/v1/search/plugins', 'plugins')
