from rest_framework import generics
from ..models import Company
from ..search import search, search_json
from .serializers import CompanySerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

# currently api v1 us on;
# to change to 2 has to uncomment lines after api v2 in base.html and to comment lines after api v 1 - 3 lines

#http://localhost/api/v1/company/?q=
# api v1
class CompanyList(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    def get_queryset(self):
        q = self.request.query_params.get('q')
        if q is not None:
            return search(q)
        return super().get_queryset()

#http://localhost/api/v2/company/?q=
# api v2
class CompanyListJson(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    def get(self, request, format=None):
        q = request.GET.get('q')
        content = search_json(q)
        return Response(content)


