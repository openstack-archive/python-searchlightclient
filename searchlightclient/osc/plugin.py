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

import logging

from openstackclient.common import utils

LOG = logging.getLogger(__name__)

DEFAULT_SEARCH_API_VERSION = '1'
API_VERSION_OPTION = 'os_search_api_version'
API_NAME = 'search'
API_VERSIONS = {
    '1': 'searchlightclient.v1.client.Client',
}


def make_client(instance):
    """Returns a search service client"""
    search_client = utils.get_client_class(
        API_NAME,
        instance._api_version[API_NAME],
        API_VERSIONS)

    client = search_client(
        endpoint=instance.get_endpoint_for_service_type('search'),
        session=instance.session,
        auth_url=instance._auth_url,
        username=instance._username,
        password=instance._password,
        region_name=instance._region_name,
    )

    return client


def build_option_parser(parser):
    """Hook to add global options"""
    parser.add_argument(
        '--os-search-api-version',
        metavar='<search-api-version>',
        default=utils.env(
            'OS_SEARCH_API_VERSION',
            default=DEFAULT_SEARCH_API_VERSION),
        help='Search API version, default=' +
             DEFAULT_SEARCH_API_VERSION +
             ' (Env: OS_SEARCH_API_VERSION)')
    return parser
