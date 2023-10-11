import json

from django.test import TestCase
from django.urls import reverse
from noticias.models import Noticias
from rest_framework import status


class NoticiasDetailReatriveTest(TestCase):
    def setUp(self) -> None:
        self.valores = {
            'titulo': 'Teste',
            'conteudo': 'Teste',
            'autor': 'Teste',
            'publicado': True,
        }
        Noticias.objects.create(**self.valores)

    def test_noticias__detail_retorna_status_code_200_ok(self):
        noticia = Noticias.objects.all().first()
        resposta = self.client.get(reverse(
            'noticias-detail', args={noticia.id}
        ))
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)

    def test_noticias__detail_retorna_status_code_404_not_found(self):
        resposta = self.client.get(reverse(
            'noticias-detail', args={'1327c824-2ae7-4f1d-b869-4f1a564e1fd8'}
        ))
        self.assertEqual(resposta.status_code, status.HTTP_404_NOT_FOUND)

    def test_noticias__detail_retorna_status_code_405_method_not_allowed(self):
        resposta = self.client.post(reverse(
            'noticias-detail', args={'1327c824-2ae7-4f1d-b869-4f1a564e1fd8'}
        ))
        self.assertEqual(
            resposta.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def teste_noticias__detail_titulo_da_instancia(self):
        noticia = Noticias.objects.all().first()
        self.assertEqual(noticia.__str__(), self.valores['titulo'])

    def teste_noticias__detail_nao_cadastrada(self):
        resposta = self.client.get(
            reverse(
                'noticias-detail',
                args={'1327c824-2ae7-4f1d-b869-4f1a564e1fd8'}
            )
        )
        mensagem = json.loads(resposta.content)
        self.assertEqual(
            mensagem['detail'], 'Não encontrado.'
        )

    def teste_noticia__detail_retorna_json(self):
        noticia = Noticias.objects.all().first()
        resposta = self.client.get(reverse(
            'noticias-detail', args={noticia.id}
        ))
        self.assertEqual(resposta['Content-Type'], 'application/json')


class NoticiasDetailUpdateTest(TestCase):
    def setUp(self) -> None:
        self.valores = {
            'titulo': 'Teste',
            'conteudo': 'Teste',
            'autor': 'Teste',
            'publicado': True,
        }
        Noticias.objects.create(**self.valores)
        self.noticia = Noticias.objects.all().first()

    def test_noticias__detail_retorna_status_code_200_ok(self):
        valores = {
            'titulo': 'novo',
            'conteudo': 'novo',
            'autor': 'novo',
            'publicado': False,
        }
        url = reverse('noticias-detail', args={self.noticia.id})
        resposta = self.client.put(
            url, data=valores, content_type='application/json'
        )
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)

    def test_noticias__detail_retorna_status_code_404_not_found(self):
        url = reverse(
            'noticias-detail', args={'1327c824-2ae7-4f1d-b869-4f1a564e1fd8'}
        )
        resposta = self.client.put(
            url, data=self.valores, content_type='application/json'
        )
        self.assertEqual(resposta.status_code, status.HTTP_404_NOT_FOUND)

    def test_noticias__detail_retorna_status_code_405_method_not_allowed(self):
        url = reverse(
            'noticias-detail', args={'1327c824-2ae7-4f1d-b869-4f1a564e1fd8'}
        )
        resposta = self.client.post(
            url, data=self.valores, content_type='application/json'
        )
        self.assertEqual(
            resposta.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def teste_noticias__detail_atualizacao_parcial_retorna_status_200_ok(self):
        url = reverse(
            'noticias-detail', args={self.noticia.id}
        )
        resposta = self.client.patch(
            url, data=self.valores, content_type='application/json'
        )
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)


class NoticiasDetailDestroyTest(TestCase):
    def setUp(self) -> None:
        self.valores = {
            'titulo': 'Teste',
            'conteudo': 'Teste',
            'autor': 'Teste',
            'publicado': True,
        }
        Noticias.objects.create(**self.valores)
        self.noticia = Noticias.objects.all().first()

    def test_noticias__detail_retorna_status_code_204_no_content(self):
        url = reverse('noticias-detail', args={self.noticia.id})
        resposta = self.client.delete(url)
        self.assertEqual(resposta.status_code, status.HTTP_204_NO_CONTENT)
