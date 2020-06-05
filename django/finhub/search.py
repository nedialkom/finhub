# https://github.com/elastic/elasticsearch-dsl-py
# https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html
from .documents import CompanyDocument
from elasticsearch import Elasticsearch

# Endpoint http://localhost/api/v2/company/?q=
def search_json(phrase):
    client = Elasticsearch([{'host': 'es', 'port': 9200}])
    response = client.search(
        index="company",
        body={
          "query": {
            "multi_match": {
              "query": phrase,
              "type": "cross_fields",
              "fields": ['description', 'displaySymbol', 'symbol', 'exchange'],
              "operator": "and"
            }
          }
        }
    )
    return response

# Endpoint http://localhost/api/v1/company/?q=
def get_search_query(phrase):
    query = CompanyDocument.search().query(
        "multi_match",
        query=phrase,
        fields=['description', 'displaySymbol', 'symbol', 'exchange'],
        type="cross_fields",
        operator="and"
    )
    return query

def search(phrase):
    return get_search_query(phrase).to_queryset()