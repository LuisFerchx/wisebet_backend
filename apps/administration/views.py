from rest_framework import viewsets
from .models import Agency
from .serializers import AgencySerializer

class AgencyViewSet(viewsets.ModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
