from conectorDB import conectar_banco_de_dados, fechar_conexao

def atualiza_banco(usuario, status_nome, status, cargos_id):

    conexao, banco_nome = conectar_banco_de_dados('tihd')
    if conexao:

        try:
            cursor = conexao.cursor()

            comando = (f"UPDATE glpi_users SET usertitles_id = {status} WHERE name LIKE '%{usuario}%';")

            cursor.execute(comando)

            conexao.commit()

            linhas_afetadas = cursor.rowcount
            
            if linhas_afetadas == 0:
                print(usuario, 'não encontrado/alterado')
                comando_select = (f"SELECT usertitles_id FROM glpi_users WHERE name LIKE '%{usuario}%';")
                cursor.execute(comando_select)
                resultado = cursor.fetchall()
                if not resultado:
                    print(f"Usuário {usuario} não encontrado no banco")
                    return 'não encontrado', 'N/A'
                else:
                    id_cargo = resultado[0][0]
                    print(f"Usuário {usuario} encontrado - id_cargo: {id_cargo}")
                    nome_cargo = next((chave for chave, valor in cargos_id.items() if valor == id_cargo), None)
                    return nome_cargo, id_cargo
            else:
                print(usuario, 'foi definido como', status_nome,'(', status, ') - ', banco_nome)
                return status_nome, status
            

        except Exception as erro:
            print("Erro: ", erro)
            return 'Erro', 'Erro'

        finally:
            cursor.close()
            fechar_conexao(conexao)
