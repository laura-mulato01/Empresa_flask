import mysql.connector

def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="empresa_flask"
    )

if __name__ == "__main__":
    try:
        conexao = conectar_banco()
        print("Conectado ao MySQL com sucesso!")
        conexao.close()
    except Exception as erro:
        print("Erro ao conectar:", erro)