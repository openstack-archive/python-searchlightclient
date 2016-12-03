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

"""Searchlight v1 Facet action implementations"""

import logging

from osc_lib.command import command
from osc_lib import utils


class ListFacet(command.Lister):
    """List Searchlight Facet."""

    log = logging.getLogger(__name__ + ".ListFacet")

    def get_parser(self, prog_name):
        parser = super(ListFacet, self).get_parser(prog_name)
        parser.add_argument(
            "--type",
            metavar="<resource-type>",
            help="Get facets for a particular resource type"
        )
        parser.add_argument(
            "--limit-terms",
            metavar="<limit>",
            help="Restricts the number of options returned for "
                 "fields that support facet terms"
        )
        parser.add_argument(
            "--all-projects",
            action='store_true',
            default=False,
            help="Request facet terms for all projects (admin only)"
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)

        search_client = self.app.client_manager.search
        columns = (
            "Resource Type",
            "Type",
            "Name",
            "Options"
        )
        params = {
            "type": parsed_args.type,
            "limit_terms": parsed_args.limit_terms,
            "all_projects": parsed_args.all_projects
        }
        data = search_client.facets.list(**params)
        result = []
        for resource_type, values in data.items():
            if isinstance(values, list):
                # Cope with pre-1.0 service APIs
                facets = values
            else:
                facets = values['facets']
            for s in facets:
                options = []
                for o in s.get('options', []):
                    options.append(
                        str(o['key']) + '(' + str(o['doc_count']) + ')')
                s["options"] = ', '.join(options)
                s["resource_type"] = resource_type
                result.append(utils.get_dict_properties(s, columns))
        return (columns, result)
