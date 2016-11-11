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

from six.moves.urllib import parse

from searchlightclient.common import base


class Facets(base.Resource):
    def __repr__(self):
        return "<Facets %s>" % self._info

    def list(self, **kwargs):
        return self.manager.list(self, **kwargs)


class FacetsManager(base.BaseManager):
    resource_class = Facets

    def list(self, **kwargs):
        """Get a list of facets.
        :param index: Index name to query.
        :param all_projects: By default, facet terms are limited to the
                             currently scoped project. Administrators are
                             able to request facet terms for all projects
                             by specify all_projects=True.
        :param limit_terms: Limit the number of options returned for fields
                            that support facet terms.
        :param type: Request facets for a particular type by adding a type
                     query parameter.
        :rtype: dict of {resource_type: {'facets': [:class:`Facets`],
                                         'doc_count':, :class:int}}
        """
        params = {}
        if kwargs.get('index'):
            params['index'] = kwargs['index']
        if kwargs.get('type'):
            params['type'] = kwargs['type']
        if kwargs.get('limit_terms'):
            params['limit_terms'] = kwargs['limit_terms']
        if kwargs.get('all_projects') is not None:
            params['all_projects'] = kwargs['all_projects']
        url = '/v1/search/facets?%s' % parse.urlencode(params, True)
        return self.client.get(url).json()
