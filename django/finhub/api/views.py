from rest_framework import generics
from ..models import Company
from ..search import search
from .serializers import CompanySerializer
class CompanyList(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    def get_queryset(self):
        q = self.request.query_params.get('q')
        if q is not None:
            return search(q)
        return super().get_queryset()