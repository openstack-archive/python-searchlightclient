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

from keystoneclient import adapter

from searchlightclient.common import utils
from searchlightclient import exc


def Client(version, *args, **kwargs):
    module = utils.import_versioned_module(version, 'client')
    client_class = getattr(module, 'Client')
    return client_class(*args, **kwargs)


def _construct_http_client(**kwargs):
    kwargs = kwargs.copy()
    if kwargs.get('session') is None:
        raise ValueError("A session instance is required")

    return SessionClient(
        session=kwargs.get('session'),
        auth=kwargs.get('auth'),
        region_name=kwargs.get('region_name'),
        service_type=kwargs.get('service_type', 'search'),
        interface=kwargs.get('endpoint_type', 'public').rstrip('URL'),
        user_agent=kwargs.get('user_agent', 'python-searchlightclient'),
        endpoint_override=kwargs.get('endpoint_override'),
        timeout=kwargs.get('timeout')
    )


class SessionClient(adapter.LegacyJsonAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = kwargs.pop('timeout', None)
        super(SessionClient, self).__init__(*args, **kwargs)

    def request(self, *args, **kwargs):
        kwargs.setdefault('raise_exc', True)

        if self.timeout is not None:
            kwargs.setdefault('timeout', self.timeout)

        kwargs.setdefault('headers', {}).setdefault(
            'Content-Type', 'application/json')

        resp, body = super(SessionClient, self).request(*args, **kwargs)

        if kwargs.get('raise_exc') and resp.status_code >= 400:
            raise exc.from_response(resp, body)
        return resp
