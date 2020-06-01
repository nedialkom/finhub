from elasticsearch_dsl.query import Q, MultiMatch, SF
from .documents import CompanyDocument

def get_search_query(phrase):
    query = Q(
        'function_score',
        query=MultiMatch(
            fields=['description', 'displaySymbol', 'symbol'],
            query=phrase
        ),
    )
    return CompanyDocument.search().query(query)
def search(phrase):
    return get_search_query(phrase).to_queryset()

