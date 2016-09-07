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

from searchlightclient.osc.v1 import search
from searchlightclient.tests.unit.osc import fakes
from searchlightclient.tests.unit.osc.v1 import fakes as searchlight_fakes


class TestSearch(searchlight_fakes.TestSearchv1):
    def setUp(self):
        super(TestSearch, self).setUp()
        self.search_client = self.app.client_manager.search.search


class TestSearchResource(TestSearch):

    def setUp(self):
        super(TestSearchResource, self).setUp()
        self.cmd = search.SearchResource(self.app, None)
        fake_data = copy.deepcopy(searchlight_fakes.Resource)
        fake_data['hits']['hits'][0]['is_not_processed'] = 'foo'
        self.search_client.search.return_value = \
            fakes.FakeResource(None, fake_data, loaded=True)

    def _test_search(self, arglist, **assertArgs):
        parsed_args = self.check_parser(self.cmd, arglist, [])
        columns, data = self.cmd.take_action(parsed_args)
        details = False
        if assertArgs.get("source"):
            details = True
            if assertArgs.get("source") == "all_resources":
                assertArgs.pop("source")
            else:
                assertArgs["_source"] = assertArgs.pop("source")
        self.search_client.search.assert_called_with(**assertArgs)

        if details:
            collist = ("ID", "Score", "Type", "Source")
            datalist = (
                ('1', 0.3, 'OS::Glance::Image',
                 {'id': '1', 'name': 'image1',
                  'updated_at': '2016-01-01T00:00:00Z'}),
                ('2', 0.3, 'OS::Nova::Server',
                 {'id': '2', 'name': 'instance1',
                  'updated_at': '2016-01-01T00:00:00Z'}))
        else:
            collist = ("ID", "Name", "Score", "Type", "Updated")
            datalist = (('1', 'image1', 0.3, 'OS::Glance::Image',
                         '2016-01-01T00:00:00Z'),
                        ('2', 'instance1', 0.3, 'OS::Nova::Server',
                         '2016-01-01T00:00:00Z'))

        self.assertEqual(collist, columns)
        self.assertEqual(datalist, tuple(data))

    def test_search(self):
        self._test_search(["name: fake"],
                          query={"query_string": {"query": "name: fake"}},
                          _source=['id', 'name', 'updated_at'],
                          all_projects=False, type=None)

    def test_search_resource(self):
        self._test_search(["name: fake", "--type", "res1", "res2"],
                          query={"query_string": {"query": "name: fake"}},
                          _source=['id', 'name', 'updated_at'],
                          type=["res1", "res2"],
                          all_projects=False)

    def test_search_query_string(self):
        self._test_search(["name: fake"],
                          query={"query_string": {"query": "name: fake"}},
                          _source=['id', 'name', 'updated_at'],
                          all_projects=False, type=None)

    def test_search_regexp_slashes_in_query_string(self):
        """Escape slashes in querystrings so not to be treated as regexp"""
        self._test_search(["this/has/some/slashes"],
            query={"query_string": {"query": "this\/has\/some\/slashes"}},
            _source=['id', 'name', 'updated_at'],
            all_projects=False, type=None)

    def test_search_regexp_slashes_in_query(self):
        """Don't escape slashes in DSL queries"""
        self._test_search(['--json',
                           '{"term": {"name": "this/has/some/slashes"}}'],
            query={"term": {"name": "this/has/some/slashes"}},
            _source=['id', 'name', 'updated_at'],
            all_projects=False, type=None)

    def test_search_query_dsl(self):
        self._test_search(['--json',
                           '{"term": {"status": "active"}}'],
                          query={'term': {'status': 'active'}},
                          _source=['id', 'name', 'updated_at'],
                          all_projects=False, type=None)

    def test_search_query_dsl_no_json_flag(self):
        self.assertRaises(
            SystemExit, self._test_search,
            ['{"term": {"status": "active"}}'],
            query={'term': {'status': 'active'}},
            _source=['id', 'name', 'updated_at'],
            all_projects=False, type=None)

    def test_list_all_projects(self):
        self._test_search(["name: fake", "--all-projects"],
                          query={"query_string": {"query": "name: fake"}},
                          _source=['id', 'name', 'updated_at'],
                          all_projects=True, type=None)

    def test_list_source(self):
        self._test_search(["name: fake", "--source"],
                          query={"query_string": {"query": "name: fake"}},
                          all_projects=False, source="all_resources",
                          type=None)

    def test_list_optional_source(self):
        self._test_search(["name: fake", "--source", "f1,f2"],
                          query={"query_string": {"query": "name: fake"}},
                          all_projects=False, source=["id", "f1", "f2"],
                          type=None)
