import pandas as pd
import os
from datetime import datetime

def pega_dados_planilha(sheet_id, sheet_gid, linhas_puladas, colunas_usadas):
    try:

        url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx&gid={sheet_gid}'

        df = pd.read_excel(url, skiprows = linhas_puladas, usecols = colunas_usadas)

        linhas_com_nulos = df.isnull().sum(axis = 1)
        filtro_funcionarios = df[linhas_com_nulos > 0].index

        df.drop(filtro_funcionarios, axis = 0, inplace = True)

        df.reset_index(drop = True, inplace = True)

        df[colunas_usadas[0]] = df[colunas_usadas[0]].astype(str)
        df[colunas_usadas[0]] = df[colunas_usadas[0]].apply(lambda x: x.replace(' ', '').replace('-', '')[:-1] if isinstance(x, str) else x[:-1])

        return df
    except Exception as e:
        print('Erro: ', e)


def pega_dados_planilha_local(nome_arquivo, nome_folha, linhas_puladas, colunas_usadas):
    try:

        df = pd.read_excel(nome_arquivo, sheet_name = nome_folha, skiprows = linhas_puladas, usecols = colunas_usadas)

        linhas_com_nulos = df.isnull().sum(axis = 1)
        filtro_funcionarios = df[linhas_com_nulos > 0].index

        df.drop(filtro_funcionarios, axis = 0, inplace = True)

        df.reset_index(drop = True, inplace = True)

        df[colunas_usadas[0]] = df[colunas_usadas[0]].astype(str)
        df[colunas_usadas[0]] = df[colunas_usadas[0]].apply(lambda x: x.replace(' ', '').replace('-', '')[:-1] if isinstance(x, str) else x[:-1])

        return df
    except Exception as e:
        print('Erro: ', e)


def relatorio_logs(tabelas, nomes_arquivos):

    data = datetime.now()
    data_atual = data.strftime('%d-%m-%Y_%H-%M-%S')

    try:
        dir = f'logs/{data_atual}'

        if not os.path.exists(dir):
            os.makedirs(dir)

        for tabela, arquivo in zip(tabelas, nomes_arquivos):

            tabela.to_excel(f'{dir}/{arquivo}__{data_atual}.xlsx', index = False)
        
            print(f'logs de {arquivo} salvos com sucesso!!!')

    except Exception as e:
        print(f'logs não foram salvos devido a um erro')
        print('Erro', e)
