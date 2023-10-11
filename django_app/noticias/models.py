import uuid

from django.db import models


class Noticias(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=255)
    conteudo = models.TextField()
    autor = models.CharField(max_length=255)
    publicado = models.BooleanField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
