#   Copyright 2014 OpenStack Foundation
#
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

import mock

from searchlightclient.tests.unit.osc import fakes
from searchlightclient.tests.unit.osc import utils


ResourceType = {
    "alias-searching": "searchlight-search",
    "alias-indexing": "searchlight-listener",
    "type": "OS::Nova::Server"
}


OldFacet = {
    "OS::Nova::Server":
    [
        {"type": "string", "name": "id"},
        {"type": "date", "name": "created_at"},
    ],
}


# The alternate facet format introduced in
# https://blueprints.launchpad.net/searchlight/+spec/count-endpoint
Facet = {
    "OS::Nova::Server":
    {
        "doc_count": 2,
        "facets": [
            {"type": "string", "name": "id"},
            {"type": "date", "name": "created_at"},
        ]
    }
}


Resource = {
    "hits":
    {"hits":
        [
            {"_score": 0.3, "_type": "OS::Glance::Image", "_id": "1",
             "_source": {"id": "1", "name": "image1",
                         "updated_at": "2016-01-01T00:00:00Z"}},
            {"_score": 0.3, "_type": "OS::Nova::Server", "_id": "2_ADMIN",
             "_source": {"id": "2", "name": "instance1",
                         "updated_at": "2016-01-01T00:00:00Z"}},
        ],
     "_shards": {"successful": 5, "failed": 0, "total": 5},
     "took": 5, "timed_out": False
     }
}


class FakeSearchv1Client(object):
    def __init__(self, **kwargs):
        self.http_client = mock.Mock()
        self.http_client.auth_token = kwargs['token']
        self.http_client.management_url = kwargs['endpoint']
        self.resource_types = mock.Mock()
        self.resource_types.list = mock.Mock(return_value=[])
        self.facets = mock.Mock()
        self.facets.list = mock.Mock(return_value=[])
        self.search = mock.Mock()
        self.search.search = mock.Mock(return_value=[])


class TestSearchv1(utils.TestCommand):
    def setUp(self):
        super(TestSearchv1, self).setUp()

        self.app.client_manager.search = FakeSearchv1Client(
            endpoint=fakes.AUTH_URL,
            token=fakes.AUTH_TOKEN,
        )
