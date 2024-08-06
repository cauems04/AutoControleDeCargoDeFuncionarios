import mysql.connector

def conectar_banco_de_dados(banco_nome):
    try:
        # Estabeleça a conexão com o banco de dados
        conexao = mysql.connector.connect(
            host = "10.59.208.183",
            port = "3306",
            user = "user",
            password = "pswd",
            database = banco_nome
        )

        if conexao.is_connected():
            #print("Banco acessado: ", banco_nome)
            return conexao, banco_nome

    except mysql.connector.Error as erro:
        print("Erro ao conectar ao banco de dados:", erro)
        return None

    except Exception as e:
        print('Erro: ', e)

def fechar_conexao(conexao):
    if conexao.is_connected():
        conexao.close()
