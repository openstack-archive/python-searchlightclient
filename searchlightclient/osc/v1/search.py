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

"""Searchlight v1 Search action implementations"""

import logging
import six

from cliff import lister
from openstackclient.common import utils


class SearchResource(lister.Lister):
    """Search Searchlight resource."""

    log = logging.getLogger(__name__ + ".SearchResource")

    def get_parser(self, prog_name):
        parser = super(SearchResource, self).get_parser(prog_name)
        parser.add_argument(
            "query",
            metavar="<query>",
            help="Query resources by Elasticsearch query string "
                 "(NOTE: json format DSL is not supported yet). "
                 "Example: 'name: cirros AND updated_at: [now-1y TO now]'. "
                 "See Elasticsearch DSL or Searchlight documentation for "
                 "more detail."
        )
        parser.add_argument(
            "--type",
            nargs='*',
            metavar="<resource-type>",
            help="One or more types to search. Uniquely identifies resource "
                 "types. Example: --type OS::Glance::Image "
                 "OS::Nova::Server"
        )
        parser.add_argument(
            "--all-projects",
            action='store_true',
            default=False,
            help="By default searches are restricted to the current project "
                 "unless all_projects is set"
        )
        parser.add_argument(
            "--source",
            action='store_true',
            default=False,
            help="Whether to display the source details, defaults to false. "
                 "You can specify --max-width to make the output look better."
        )
        return parser

    @utils.log_method(log)
    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)

        search_client = self.app.client_manager.search
        mapping = {"_score": "score", "_type": "type", "_id": "id",
                   "_index": "index", "_source": "source"}

        params = {
            "type": parsed_args.type,
            "all_projects": parsed_args.all_projects
        }
        if parsed_args.source:
            columns = ("ID", "Score", "Type", "Source")
        else:
            columns = ("ID", "Name", "Score", "Type", "Updated")
            # Only return the required fields when source not specified.
            params["_source"] = ["name", "updated_at"]

        # TODO(lyj): json should be supported for query
        if parsed_args.query:
            query = {"query_string": {"query": parsed_args.query}}
            params['query'] = query

        data = search_client.search.search(**params)
        result = []
        for r in data.hits['hits']:
            converted = {}
            for k, v in six.iteritems(r):
                converted[mapping[k]] = v
                if k == "_source" and not parsed_args.source:
                    converted["name"] = v.get("name")
                    converted["updated"] = v.get("updated_at")
            result.append(utils.get_dict_properties(converted, columns))
        return (columns, result)
