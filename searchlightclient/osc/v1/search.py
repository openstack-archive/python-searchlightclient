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

from oslo_serialization import jsonutils

from osc_lib.command import command
from osc_lib import utils


class SearchResource(command.Lister):
    """Search Searchlight resource."""

    log = logging.getLogger(__name__ + ".SearchResource")

    def get_parser(self, prog_name):
        parser = super(SearchResource, self).get_parser(prog_name)
        parser.add_argument(
            "query",
            metavar="<query>",
            help="Query resources by Elasticsearch query string or json "
                 "format DSL. Query string example: 'name: cirros AND "
                 "updated_at: [now-1y TO now]'. DSL example: "
                 "'{\"term\": {\"name\": \"cirros\"}}'. "
                 "See Elasticsearch DSL or Searchlight documentation for "
                 "more detail."
        )
        parser.add_argument(
            "--json",
            action='store_true',
            default=False,
            help="Treat the query argument as a JSON formatted DSL query."
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
            nargs='?',
            const='all_sources',
            metavar="[<field>,...]",
            help="Whether to display the json source. If not specified, "
                 "it will not be displayed. If specified with no argument, "
                 "the full source will be displayed. Otherwise, specify the "
                 "fields combined with ',' to return the fields you want. "
                 "It is recommended that you use the --max-width argument "
                 "with this option."
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)

        search_client = self.app.client_manager.search
        mapping = {"_score": "score", "_type": "type", "_id": "id",
                   "_index": "index", "_source": "source"}

        params = {
            "type": parsed_args.type,
            "all_projects": parsed_args.all_projects
        }
        source = parsed_args.source
        if source:
            columns = ("ID", "Score", "Type", "Source")
            if source != "all_sources":
                params["_source"] = (["id"] +
                    [s for s in source.split(",") if s != 'id'])
        else:
            columns = ("ID", "Name", "Score", "Type", "Updated")
            # Only return the required fields when source not specified.
            params["_source"] = ["id", "name", "updated_at"]

        if parsed_args.query:
            if parsed_args.json:
                query = jsonutils.loads(parsed_args.query)
            else:
                try:
                    jsonutils.loads(parsed_args.query)
                    print("You should use the --json flag when specifying "
                          "a JSON object.")
                    exit(1)
                except Exception:
                    qs = self._modify_query_string(parsed_args.query)
                    query = {"query_string": {"query": qs}}

            params['query'] = query

        data = search_client.search.search(**params)
        result = []
        for r in data.hits['hits']:
            converted = {}
            extra = {}
            # hit._id may include extra information appended after _,
            # so use r['_source']['id'] for safe.
            r['_id'] = r.get('_source', {}).get('id')
            for k, v in r.items():
                map_key = mapping.get(k)
                if map_key is not None:
                    converted[map_key] = v
                    if k == "_source" and not parsed_args.source:
                        converted["name"] = v.get("name")
                        converted["updated"] = v.get("updated_at")
                else:
                    extra[k] = v
            if extra:
                self.log.debug("extra info returned: %s", extra)
            result.append(utils.get_dict_properties(converted, columns))
        return (columns, result)

    def _modify_query_string(self, query_string):
        return query_string.replace('/', '\/')
