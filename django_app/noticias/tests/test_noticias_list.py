import json

from django.test import TestCase
from django.urls import reverse
from noticias.models import Noticias
from rest_framework import status


class NoticiasListTeste(TestCase):
    def setUp(self) -> None:
        self.valores = {
            'titulo': 'Teste',
            'conteudo': 'Teste',
            'autor': 'Teste',
            'publicado': True,
        }

    def teste_noticias__list_retorna_status_code_200_ok(self):
        resposta = self.client.get(reverse('noticias-list'))
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)

    def teste_noticias__list_retorna_status_code_400_bad_request(self):
        url = reverse('noticias-list')
        resposta = self.client.post(url, data={})
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)

    def teste_noticias__list_retorna_json(self):
        resposta = self.client.get(reverse('noticias-list'))
        self.assertEqual(resposta['Content-Type'], 'application/json')

    def teste_noticias_cadastrada_com_sucesso(self):
        url = reverse('noticias-list')
        resposta = self.client.post(url, data=self.valores)
        dicionario = json.loads(resposta.content)

        for chave, valor in self.valores.items():
            with self.subTest():
                self.assertEqual(dicionario[chave], valor)

    def teste_noticias_cadastrada_retorna_status_code_201_created(self):
        url = reverse('noticias-list')
        resposta = self.client.post(url, data=self.valores)
        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)

    def teste_noticias_campo_titulo_deve_ter_ate_255_caracteres(self):
        self.valores['titulo'] = 'a' * 256
        url = reverse('noticias-list')
        resposta = self.client.post(url, data=self.valores)
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)

    def teste_noticias_mensagem_erro_de_tamanho_maximo_no_campo_titulo(self):
        self.valores['titulo'] = 'a' * 256
        url = reverse('noticias-list')
        resposta = self.client.post(url, data=self.valores)
        mensagem = json.loads(resposta.content)

        self.assertEqual(
            mensagem['titulo'][0],
            'Certifique-se de que este campo não tenha mais de 255 caracteres.'  # noqa
        )

    def teste_noticias_mensagem_erro_de_tamanho_maximo_no_campo_autor(self):
        self.valores['autor'] = 'a' * 256
        url = reverse('noticias-list')
        resposta = self.client.post(url, data=self.valores)
        mensagem = json.loads(resposta.content)

        self.assertEqual(
            mensagem['autor'][0],
            'Certifique-se de que este campo não tenha mais de 255 caracteres.'  # noqa
        )

    def teste_noticias_mensagem_erro_todos_os_campos_sao_obrigatorios(self):
        valores = {}
        url = reverse('noticias-list')
        resposta = self.client.post(url, data=valores)
        mensagem = json.loads(resposta.content)

        for campo in ['titulo', 'conteudo', 'autor']:
            with self.subTest():
                self.assertEqual(
                    mensagem[campo][0], 'Este campo é obrigatório.'
                )

    def teste_noticias_mensagem_erro_campos_em_branco(self):
        valores = {
            'titulo': '',
            'conteudo': '',
            'autor': '',
        }
        url = reverse('noticias-list')
        resposta = self.client.post(url, data=valores)
        mensagem = json.loads(resposta.content)

        for campo, _ in valores.items():
            self.assertEqual(
                mensagem[campo][0],
                'Este campo não pode ser em branco.'
            )

    def teste_campo_publicado_deve_ser_booleano(self):
        self.valores['publicado'] = ''
        url = reverse('noticias-list')
        resposta = self.client.post(url, data=self.valores)
        mensagem = json.loads(resposta.content)

        self.assertEqual(
            mensagem['publicado'][0], 'Must be a valid boolean.'
        )

    def teste_noticias_list_retorna_quantidade_cadastradas(self):
        Noticias.objects.create(**self.valores)
        noticias = Noticias.objects.all()
        self.assertEqual(len(noticias), 1)
