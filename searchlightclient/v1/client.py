#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from searchlightclient import client
from searchlightclient.v1 import facets
from searchlightclient.v1 import resource_types
from searchlightclient.v1 import search


class Client(object):
    """Client for the Searchlight v1 API.

    :param session: a keystoneauth/keystoneclient session object
    :type session: keystoneclient.session.Session
    :param str service_type: The default service_type for URL discovery
    :param str interface: The default interface for URL discovery
                          (Default: public)
    :param str region_name: The default region_name for URL discovery
    :param str endpoint_override: Always use this endpoint URL for requests
                                  for this ceiloclient
    :param auth: An auth plugin to use instead of the session one
    :type auth: keystoneclient.auth.base.BaseAuthPlugin
    :param str user_agent: The User-Agent string to set
                           (Default is python-searchlightclient)
    """

    def __init__(self, *args, **kwargs):
        """Initialize a new client for the Searchlight v1 API."""
        self.http_client = client._construct_http_client(*args, **kwargs)
        self.resource_types = resource_types.ResourceTypeManager(
            self.http_client)
        self.facets = facets.FacetsManager(self.http_client)
        self.search = search.SearchManager(self.http_client)
