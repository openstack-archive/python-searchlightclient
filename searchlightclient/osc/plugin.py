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

"""OpenStackClient plugin for Search service."""

import logging

from osc_lib import utils

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

    # Set client http_log_debug to True if verbosity level is high enough
    http_log_debug = utils.get_effective_log_level() <= logging.DEBUG

    # Remember interface only if it is set
    kwargs = utils.build_kwargs_dict('endpoint_type', instance._interface)
    client = search_client(
        session=instance.session,
        http_log_debug=http_log_debug,
        region_name=instance._region_name,
        **kwargs
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
