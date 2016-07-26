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

from searchlightclient.osc.v1 import facet
from searchlightclient.tests.unit.osc.v1 import fakes as searchlight_fakes


class TestFacet(searchlight_fakes.TestSearchv1):
    def setUp(self):
        super(TestFacet, self).setUp()
        self.facet_client = self.app.client_manager.search.facets


class TestFacetListBase(TestFacet):
    def setUp(self):
        super(TestFacetListBase, self).setUp()
        self.cmd = facet.ListFacet(self.app, None)
        self.facet_client.list.return_value = searchlight_fakes.Facet

    def _test_list(self, arglist, **assertArgs):
        parsed_args = self.check_parser(self.cmd, arglist, [])
        columns, data = self.cmd.take_action(parsed_args)
        self.facet_client.list.assert_called_with(**assertArgs)

        collist = ('Resource Type', 'Type', 'Name', 'Options')
        self.assertEqual(collist, columns)

        datalist = (
            ('OS::Nova::Server', 'string', 'id', ''),
            ('OS::Nova::Server', 'date', 'created_at', ''),
        )
        self.assertEqual(datalist, tuple(data))


class TestFacetList(TestFacetListBase):
    def test_list(self):
        self._test_list([], all_projects=False, limit_terms=None, type=None)

    def test_list_all_projects(self):
        self._test_list(['--all-projects'],
                        all_projects=True, limit_terms=None, type=None)

    def test_list_with_type(self):
        self._test_list(['--type', 'fake_res_type'],
                        all_projects=False,
                        limit_terms=None, type='fake_res_type')

    def test_list_with_limit_terms(self):
        self._test_list(['--limit-terms', 'fake_limit'],
                        all_projects=False,
                        limit_terms='fake_limit', type=None)


class TestOldFacetList(TestFacetListBase):
    def setUp(self):
        super(TestOldFacetList, self).setUp()
        self.facet_client.list.return_value = searchlight_fakes.OldFacet

    def test_list(self):
        self._test_list([], all_projects=False, limit_terms=None, type=None)
