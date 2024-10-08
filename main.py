import pandas as pd
import schedule
from dados_planilha import pega_dados_planilha, pega_dados_planilha_local, relatorio_logs
from consultasDB import atualiza_banco

pd.set_option('display.max_rows', None)

def atualiza_coordenador(dados, dicionario_cargos, tabela_relatorio, coordenadores):
    try:
        for i in range(0, len(dados)):
            rf = dados[dados.columns[0]].iloc[i]
            cargo = ''
            cargo_id = None

            if dados[dados.columns[1]].iloc[i] == 1:
                cargo = 'Coordenador'
                cargo_id = dicionario_cargos[cargo]

                coordenadores.append(rf)
                cargo, cargo_id  = atualiza_banco(rf, cargo, cargo_id, dicionario_cargos)
                
                tabela_relatorio = pd.concat([tabela_relatorio, pd.DataFrame({'RF': [rf], 'Cargo_atualizado': [cargo], 'Cargo_ID': cargo_id})], ignore_index = True)
            else:
                print(rf, 'não é coordenador')
            
        return coordenadores, tabela_relatorio
    except Exception as e:
        print('Erro: ', e)


def atualiza_funcionarios(dados, dicionario_cargos, tabela_relatorio, tabela_cargos_inexistentes, coordenadores):
    try:
        for i in range(0, len(dados)):

            rf = dados[dados.columns[0]].loc[i]
            cargo = ''
            cargo_id = None

            if rf not in coordenadores:
                cargo = dados[dados.columns[1]].loc[i]

                if cargo in dicionario_cargos.keys():
                    cargo_id = dicionario_cargos[cargo]

                    cargo, cargo_id  = atualiza_banco(rf, cargo, cargo_id, dicionario_cargos)

                    tabela_relatorio = pd.concat([tabela_relatorio, pd.DataFrame({'RF': [rf], 'Cargo_atualizado': [cargo], 'Cargo_ID': cargo_id})], ignore_index = True)
                else:
                    print(f'Cargo {cargo} do usuário {rf} não existe no banco')
                    tabela_cargos_inexistentes = pd.concat([tabela_cargos_inexistentes, pd.DataFrame({'RF': [rf], 'Cargo': [cargo]})], ignore_index = True)

            else:
                print(f'{rf} já é coordenador')

        return tabela_relatorio, tabela_cargos_inexistentes
        
    except Exception as e:
        print('Erro: ', e)
        return tabela_relatorio, tabela_cargos_inexistentes


def atualiza_cargos():

    tabela_coordenadores_atualizados = pd.DataFrame(columns = ['col1', 'col2', 'col3'])
    tabela_funcionarios_atualizados = pd.DataFrame(columns = ['col1', 'col2', 'col3'])
    tabela_cargos_nao_identificados = pd.DataFrame(columns = ['col1', 'col2'])

    cargos_ids = {'Coordenador': 3, 'Operacional/Fundamental': 8, 'Bibliotecário': 9, 'Superior': 12, 'Administrativo/Nível Médio': 13, 'Operacional/Fundamental - Vigia': 14}

    try:
        #Para a criação de uma tabela vinda da planilha, sempre informar a primeira coluna sendo o rf(REGISTRO FUNCIONAL) do jeito que é apresentado na planilha original
        '''
        dados_estrutura = pega_dados_planilha('teste', 'teste', teste, ['teste'])
        dados_biblioteca = pega_dados_planilha('teste', 'teste', teste, ['teste'])
        dados_funcionarios = pega_dados_planilha('teste', 'teste', teste, ['teste'])
        '''
        dados_estrutura = pega_dados_planilha_local('teste.xlsx', 'teste', 1, ['teste'])
        print(dados_estrutura)
        dados_biblioteca = pega_dados_planilha_local('teste.xlsx', 'teste', 1, ['teste'])
        print(dados_biblioteca)
        dados_funcionarios = pega_dados_planilha_local('teste.xlsx', 'teste', None, ['teste'])
        print(dados_funcionarios)

        coordenadores = []

        coordenadores, tabela_coordenadores_atualizados = atualiza_coordenador(dados_estrutura, cargos_ids, tabela_coordenadores_atualizados, coordenadores)
        print(coordenadores)
        coordenadores, tabela_coordenadores_atualizados = atualiza_coordenador(dados_biblioteca, cargos_ids, tabela_coordenadores_atualizados, coordenadores)
        print(coordenadores)

        tabela_funcionarios_atualizados, tabela_cargos_nao_identificados = atualiza_funcionarios(dados_funcionarios, cargos_ids, tabela_funcionarios_atualizados, tabela_cargos_nao_identificados, coordenadores)

        print('\n\n--------------Funcionários atualizados--------------')
        print(tabela_funcionarios_atualizados)
        print('__________________________________________________________\n\n')

        print('\n--Funcionários com cargos não identificados--')
        print(tabela_cargos_nao_identificados)
        print('__________________________________________________________\n\n')

        print('\n-----Coordenadores atualizados-----')
        print(tabela_coordenadores_atualizados)

        return tabela_coordenadores_atualizados, tabela_funcionarios_atualizados, tabela_cargos_nao_identificados

    except Exception as e:
        print('Erro: ', e)

relatorio_coordenadores, relatorio_funcionarios, relatorio_cargos_nao_identificados = atualiza_cargos()

relatorio_logs([relatorio_coordenadores, relatorio_funcionarios, relatorio_cargos_nao_identificados], ['Coordenadores atualizados', 'Funcionarios atualizados', 'Exceções'])

#schedule.every(1).friday.do(atualiza_cargos)

#while True:
#    schedule.run_pending()
