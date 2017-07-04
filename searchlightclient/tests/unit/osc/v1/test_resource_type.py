#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import copy

from searchlightclient.osc.v1 import resource_type
from searchlightclient.tests.unit.osc import fakes
from searchlightclient.tests.unit.osc.v1 import fakes as searchlight_fakes


class TestResourceType(searchlight_fakes.TestSearchv1):
    def setUp(self):
        super(TestResourceType, self).setUp()
        self.rtype_client = self.app.client_manager.search.resource_types


class TestResourceTypeList(TestResourceType):

    def setUp(self):
        super(TestResourceTypeList, self).setUp()
        self.cmd = resource_type.ListResourceType(self.app, None)
        self.rtype_client.list.return_value = [
            fakes.FakeResource(
                None,
                copy.deepcopy(searchlight_fakes.ResourceType),
                loaded=True,
            ),
        ]

    def test_list(self):
        parsed_args = self.check_parser(self.cmd, [], [])
        columns, data = self.cmd.take_action(parsed_args)
        self.rtype_client.list.assert_called_with()

        collist = ('Alias Searching', 'Alias Indexing', 'Type')
        self.assertEqual(collist, columns)

        datalist = (('searchlight-search',
                     'searchlight-listener',
                     'OS::Nova::Server'),)
        self.assertEqual(datalist, tuple(data))
