import unittest
from unittest.mock import patch, AsyncMock
import asyncio

# Adicione o diretório scripts ao sys.path para importar o módulo
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'scripts')))

from initial_data_collection import PoliticalDataCollector

class AiohttpMockResponse:
    def __init__(self, json_data, status=200):
        self._json_data = json_data
        self.status = status

    async def json(self):
        return self._json_data

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self

    def raise_for_status(self):
        pass

class TestPoliticalDataCollector(unittest.IsolatedAsyncioTestCase):

    @patch('aiohttp.ClientSession.get')
    async def test_collect_all_deputies(self, mock_get):
        # Mock da resposta da API da Câmara
        mock_get.side_effect = [
            AiohttpMockResponse({
                'dados': [{'id': '123', 'nome': 'Deputado Teste'}],
                'links': [{'rel': 'next', 'href': 'http://nextpage.com'}]
            }),
            AiohttpMockResponse({
                'dados': [{'id': '456', 'nome': 'Deputado Teste 2'}],
                'links': []
            }),
            AiohttpMockResponse({
                'dados': {
                    'id': '123',
                    'nomeCivil': 'Nome Civil Teste',
                    'ultimoStatus': {
                        'nome': 'Deputado Teste',
                        'siglaPartido': 'PT',
                        'siglaUf': 'SP',
                        'email': 'dep.teste@camara.leg.br',
                        'gabinete': {'nome': '101', 'telefone': '123456'},
                        'urlFoto': 'http://foto.url'
                    }
                }
            }),
            AiohttpMockResponse({'dados': []}),
            AiohttpMockResponse({'dados': {'id': '456'}}),
            AiohttpMockResponse({'dados': []}),
        ]

        collector = PoliticalDataCollector()
        deputies = await collector.collect_all_deputies()

        self.assertEqual(len(deputies), 2)
        self.assertEqual(deputies[0]['id'], '123')

    @patch('aiohttp.ClientSession.get')
    async def test_collect_all_senators(self, mock_get):
        # Mock da resposta da API do Senado
        mock_get.side_effect = [
            AiohttpMockResponse({
                'ListaParlamentarEmExercicio': {
                    'Parlamentares': {
                        'Parlamentar': [
                            {'IdentificacaoParlamentar': {'CodigoParlamentar': '1'}}
                        ]
                    }
                }
            }),
            AiohttpMockResponse({
                'DetalheParlamentar': {
                    'Parlamentar': {
                         'IdentificacaoParlamentar': {
                            'NomeCompletoParlamentar': 'Senador Teste Completo',
                            'NomeParlamentar': 'Senador Teste',
                            'SiglaPartidoParlamentar': 'MDB',
                            'UfParlamentar': 'RJ'
                        },
                        'Mandato': {
                            'DescricaoParticipacao': 'Titular'
                        },
                        'Emails': {
                            'Email': [
                                {'DescricaoEmail': 'senador.teste@senado.leg.br'}
                            ]
                        }
                    }
                }
            })
        ]

        collector = PoliticalDataCollector()
        senators = await collector.collect_all_senators()

        self.assertEqual(len(senators), 1)
        self.assertEqual(senators[0]['DetalheParlamentar']['Parlamentar']['IdentificacaoParlamentar']['NomeParlamentar'], 'Senador Teste')

if __name__ == '__main__':
    unittest.main()
