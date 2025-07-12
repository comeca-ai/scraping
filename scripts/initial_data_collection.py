import requests
import json
from datetime import datetime
import asyncio
import aiohttp
from typing import List, Dict
import psycopg2
from psycopg2.extras import execute_values

class PoliticalDataCollector:
    def __init__(self):
        self.camara_base_url = "https://dadosabertos.camara.leg.br/api/v2"
        self.senado_base_url = "https://legis.senado.leg.br/dadosabertos"
        try:
            self.db_conn = psycopg2.connect(
                "postgresql://user:pass@localhost/political_db"
            )
        except psycopg2.OperationalError as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            self.db_conn = None

    async def collect_all_deputies(self) -> List[Dict]:
        """Coleta todos os deputados em exercício"""
        async with aiohttp.ClientSession() as session:
            # Pegar lista completa (com paginação)
            all_deputies = []
            url = f"{self.camara_base_url}/deputados?ordem=ASC&ordenarPor=nome"

            while url:
                async with session.get(url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    all_deputies.extend(data['dados'])

                    # Verificar se há próxima página
                    links = data.get('links', [])
                    url = None
                    for link in links:
                        if link['rel'] == 'next':
                            url = link['href']
                            break

            print(f"Total de deputados coletados: {len(all_deputies)}")

            # Buscar detalhes de cada deputado
            detailed_deputies = []
            for deputy in all_deputies:
                details = await self.get_deputy_details(session, deputy['id'])
                if details:
                    detailed_deputies.append(details)
                await asyncio.sleep(0.1) # Adiciona um delay de 100ms

            return [d for d in detailed_deputies if d]

    async def get_deputy_details(self, session, deputy_id: str) -> Dict:
        """Busca detalhes completos de um deputado"""
        url = f"{self.camara_base_url}/deputados/{deputy_id}"

        try:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                deputy_data = data['dados']

                # Buscar órgãos (comissões)
                orgaos_url = f"{self.camara_base_url}/deputados/{deputy_id}/orgaos"
                async with session.get(orgaos_url) as org_response:
                    org_response.raise_for_status()
                    orgaos_data = await org_response.json()
                    deputy_data['orgaos'] = orgaos_data['dados']

                return deputy_data

        except Exception as e:
            print(f"Erro ao buscar detalhes do deputado {deputy_id}: {e}")
            return None

    async def collect_all_senators(self) -> List[Dict]:
        """Coleta todos os senadores em exercício"""
        async with aiohttp.ClientSession() as session:
            url = f"{self.senado_base_url}/senador/lista/atual"
            headers = {'Accept': 'application/json'}

            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                senators_list = data['ListaParlamentarEmExercicio']['Parlamentares']['Parlamentar']

                print(f"Total de senadores: {len(senators_list)}")

                # Buscar detalhes de cada senador
                detailed_senators = []
                for senator in senators_list:
                    details = await self.get_senator_details(
                        session,
                        senator['IdentificacaoParlamentar']['CodigoParlamentar']
                    )
                    if details:
                        detailed_senators.append(details)

                    await asyncio.sleep(0.1)

                return [s for s in detailed_senators if s]

    async def get_senator_details(self, session, senator_id: str) -> Dict:
        """Busca detalhes completos de um senador"""
        url = f"{self.senado_base_url}/senador/{senator_id}"
        headers = {'Accept': 'application/json'}
        try:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                return data
        except Exception as e:
            print(f"Erro ao buscar detalhes do senador {senator_id}: {e}")
            return None

    def save_to_database(self, politicians: List[Dict], tipo: str):
        """Salva os dados no banco de dados"""
        if not self.db_conn:
            print("Não foi possível salvar no banco de dados. Conexão não estabelecida.")
            return

        cursor = self.db_conn.cursor()

        # Preparar dados para inserção
        values = []
        for pol in politicians:
            if tipo == 'deputado':
                s = pol['ultimoStatus']
                values.append((
                    pol['id'],
                    s['nome'],
                    pol['nomeCivil'],
                    tipo,
                    s['siglaPartido'],
                    s['siglaUf'],
                    s['email'],
                    s['gabinete']['telefone'],
                    s['gabinete']['nome'],
                    s['urlFoto'],
                    True
                ))
            else:  # senador
                s = pol['DetalheParlamentar']['Parlamentar']
                i = s['IdentificacaoParlamentar']
                values.append((
                    i['CodigoParlamentar'],
                    i['NomeParlamentar'],
                    i['NomeCompletoParlamentar'],
                    tipo,
                    i['SiglaPartidoParlamentar'],
                    i['UfParlamentar'],
                    next((e['DescricaoEmail'] for e in s.get('Emails', {}).get('Email', []) if e), None),
                    None,  # Telefone não disponível na API
                    None,  # Gabinete não disponível na API
                    i['UrlFotoParlamentar'],
                    True
                ))

        # Insert com ON CONFLICT para evitar duplicatas
        insert_query = """
        INSERT INTO politicians (
            external_id, nome, nome_civil, tipo, partido,
            uf, email, telefone, gabinete, foto_url, em_exercicio
        ) VALUES %s
        ON CONFLICT (external_id)
        DO UPDATE SET
            nome = EXCLUDED.nome,
            partido = EXCLUDED.partido,
            email = EXCLUDED.email,
            updated_at = NOW()
        """

        execute_values(cursor, insert_query, values)
        self.db_conn.commit()

        print(f"{len(values)} {tipo}s salvos/atualizados no banco")

# Executar coleta
async def main():
    collector = PoliticalDataCollector()

    print("🏛️ Iniciando coleta de dados do Congresso Nacional...")

    # Coletar deputados
    print("\n📊 Coletando deputados...")
    deputies = await collector.collect_all_deputies()
    if deputies:
        collector.save_to_database(deputies, 'deputado')

    # Coletar senadores
    print("\n📊 Coletando senadores...")
    senators = await collector.collect_all_senators()
    if senators:
        collector.save_to_database(senators, 'senador')

    print("\n✅ Coleta concluída!")
    if deputies and senators:
        print(f"Total: {len(deputies)} deputados + {len(senators)} senadores")

if __name__ == "__main__":
    asyncio.run(main())
