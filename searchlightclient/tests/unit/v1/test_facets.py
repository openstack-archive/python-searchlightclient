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

from searchlightclient.v1 import facets

import mock
import testtools


class FacetsManagerTest(testtools.TestCase):

    def setUp(self):
        super(FacetsManagerTest, self).setUp()
        self.manager = facets.FacetsManager(None)
        self.manager.client = mock.Mock()

    def test_list_all_projects(self):
        self.manager.list(all_projects=True)
        self.manager.client.get.assert_called_once_with(
            '/v1/search/facets?all_projects=True')

    def test_list_by_type(self):
        self.manager.list(type='fake_type')
        self.manager.client.get.assert_called_once_with(
            '/v1/search/facets?type=fake_type')

    def test_list_by_index(self):
        self.manager.list(index='fake_index')
        self.manager.client.get.assert_called_once_with(
            '/v1/search/facets?index=fake_index')

    def test_list_by_limit_terms(self):
        self.manager.list(limit_terms='10')
        self.manager.client.get.assert_called_once_with(
            '/v1/search/facets?limit_terms=10')
