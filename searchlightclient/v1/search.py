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

from searchlightclient.common import base


class Search(base.Resource):
    def __repr__(self):
        return "<Resource %s>" % self._info

    def search(self, **kwargs):
        return self.manager.search(self, **kwargs)


class SearchManager(base.BaseManager):
    resource_class = Search

    def search(self, **kwargs):
        """Executes a search query against searchlight and returns the 'hits'
        from the response. Currently accepted parameters are (all optional):

        :param query: see Elasticsearch DSL or Searchlight documentation;
                      defaults to match everything
        :param type: one or more types to search. Uniquely identifies resource
                     types. Example: OS::Glance::Image
        :param offset: skip over this many results
        :param limit: return this many results
        :param sort: sort by one or more fields
        :param _source: restrict the fields returned for each document
        :param highlight: add an Elasticsearch highlight clause
        :param all_projects: by default searches are restricted to the
                             current project unless all_projects is set
        :param simplified: return only _source data
        """
        search_params = {}
        for k, v in kwargs.items():
            if k in ('query', 'type', 'offset',
                     'limit', 'sort', '_source', 'highlight', 'all_projects'):
                search_params[k] = v
        resources = self._post('/v1/search', search_params)

        # NOTE: This could be done at the server side to reduce data
        # transfer, since the data have been wrapped several times
        # before transfer, and the data overhead is pretty small comparing
        # to the data payload('_source'), it is done here for simplicity.
        if 'simplified' in kwargs and kwargs['simplified']:
            resources = [h['_source'] for h in resources.hits['hits']]

        return resources
