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

        dir = f'logs'

        lista_logs = [os.listdir(dir)][0]

        if len(lista_logs) >= 4:
            print(lista_logs)
            lista_logs.sort(key = lambda x: os.path.getctime(os.path.join(dir, x)), reverse = True)
            print(lista_logs)

            for log in lista_logs[1:]:
                os.remove(os.path.join(dir, log))

        log_geral_dir = os.path.join(dir, f'Logs__{data_atual}.xlsx')

        with pd.ExcelWriter(log_geral_dir, engine = 'xlsxwriter') as log_geral:
            for tabela, arquivo in zip(tabelas, nomes_arquivos):

                tabela.to_excel(log_geral, sheet_name = arquivo, index = False)

                print(f'logs de {arquivo} salvos com sucesso!!!')

        print(f'Relatório salvo em {log_geral_dir}')

        
    except Exception as e:
        print(f'logs não foram salvos devido a um erro')
        print('Erro', e)
