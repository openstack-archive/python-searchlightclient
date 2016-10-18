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

from searchlightclient.v1 import search

import mock
import testtools


class SearchManagerTest(testtools.TestCase):

    def setUp(self):
        super(SearchManagerTest, self).setUp()
        self.manager = search.SearchManager(None)
        self.manager._post = mock.Mock()

    def test_search_with_query(self):
        query_string = {
            'query_string': {
                'query': 'database'
            }
        }
        self.manager.search(query=query_string)
        self.manager._post.assert_called_once_with(
            '/v1/search', {'query': query_string})

    def test_search_with_type(self):
        self.manager.search(type='fake_type')
        self.manager._post.assert_called_once_with(
            '/v1/search', {'type': 'fake_type'})

    def test_search_with_offset(self):
        self.manager.search(offset='fake_offset')
        self.manager._post.assert_called_once_with(
            '/v1/search', {'offset': 'fake_offset'})

    def test_search_with_limit(self):
        self.manager.search(limit=10)
        self.manager._post.assert_called_once_with(
            '/v1/search', {'limit': 10})

    def test_search_with_sort(self):
        self.manager.search(sort='asc')
        self.manager._post.assert_called_once_with(
            '/v1/search', {'sort': 'asc'})

    def test_search_with_source(self):
        self.manager.search(_source=['fake_source'])
        self.manager._post.assert_called_once_with(
            '/v1/search', {'_source': ['fake_source']})

    def test_search_with_highlight(self):
        self.manager.search(highlight='fake_highlight')
        self.manager._post.assert_called_once_with(
            '/v1/search', {'highlight': 'fake_highlight'})

    def test_search_with_all_projects(self):
        self.manager.search(all_projects=True)
        self.manager._post.assert_called_once_with(
            '/v1/search', {'all_projects': True})

    def test_search_with_invalid_option(self):
        self.manager.search(invalid='fake')
        self.manager._post.assert_called_once_with('/v1/search', {})
