from rest_framework import viewsets

from .models import Noticias
from .serializers import NoticiasSerializer


class NoticiaViewSet(viewsets.ModelViewSet):
    queryset = Noticias.objects.all()
    serializer_class = NoticiasSerializer
    permission_classes = []
