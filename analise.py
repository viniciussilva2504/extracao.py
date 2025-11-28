"""
Script para extrair dados da taxa CDI do BCB e gerar visualização gráfica.

Este script realiza as seguintes operações:
1. Extrai a taxa CDI da API do Banco Central do Brasil
2. Gera 10 registros de dados com variação aleatória
3. Salva os dados em arquivo CSV
4. Gera um gráfico de linha com os dados coletados
"""

import os
import time
import json
from sys import argv
from random import random
from datetime import datetime

import requests
import pandas as pd
import seaborn as sns


def extrair_taxa_cdi():
    """
    Extrai a taxa CDI mais recente da API do BCB.
    
    Returns:
        float: Valor da taxa CDI ou None em caso de erro
    """
    url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados'
    
    try:
        response = requests.get(url=url)
        response.raise_for_status()
    except requests.HTTPError as exc:
        print("Dado não encontrado, continuando.")
        return None
    except Exception as exc:
        print("Erro, parando a execução.")
        raise exc
    else:
        dado = json.loads(response.text)[-1]['valor']
        return float(dado)


def coletar_dados(taxa_base, num_registros=10):
    """
    Coleta dados da taxa CDI adicionando variação aleatória.
    
    Args:
        taxa_base (float): Taxa base para calcular variações
        num_registros (int): Número de registros a coletar
    """
    arquivo_csv = './taxa-cdi.csv'
    
    # Verifica e cria o arquivo CSV com cabeçalho
    if not os.path.exists(arquivo_csv):
        with open(file=arquivo_csv, mode='w', encoding='utf8') as fp:
            fp.write('data,hora,taxa\n')
    
    # Coleta os dados com intervalo de 1 segundo
    for _ in range(num_registros):
        data_e_hora = datetime.now()
        data = datetime.strftime(data_e_hora, '%Y/%m/%d')
        hora = datetime.strftime(data_e_hora, '%H:%M:%S')
        
        taxa = taxa_base + (random() - 0.5)
        
        with open(file=arquivo_csv, mode='a', encoding='utf8') as fp:
            fp.write(f'{data},{hora},{taxa}\n')
        
        time.sleep(1)
    
    print("Dados coletados com sucesso.")


def gerar_grafico(nome_arquivo):
    """
    Gera gráfico de linha com os dados da taxa CDI.
    
    Args:
        nome_arquivo (str): Nome do arquivo de saída (sem extensão)
    """
    df = pd.read_csv('./taxa-cdi.csv')
    
    grafico = sns.lineplot(x=df['hora'], y=df['taxa'])
    grafico.tick_params(axis='x', rotation=90)
    grafico.get_figure().savefig(f"{nome_arquivo}.png")
    
    print(f"Gráfico salvo como {nome_arquivo}.png")


def main():
    """Função principal que orquestra a extração e visualização dos dados."""
    # Verifica se o nome do gráfico foi fornecido
    if len(argv) < 2:
        print("Uso: python analise.py <nome-do-grafico>")
        return
    
    nome_grafico = argv[1]
    
    # Extrai a taxa CDI
    taxa_cdi = extrair_taxa_cdi()
    
    if taxa_cdi is None:
        print("Não foi possível obter a taxa CDI.")
        return
    
    # Coleta os dados
    coletar_dados(taxa_base=taxa_cdi, num_registros=10)
    
    # Gera o gráfico
    gerar_grafico(nome_grafico)
    
    print("Análise concluída com sucesso!")


if __name__ == "__main__":
    main()