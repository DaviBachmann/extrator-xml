import pyodbc
import pandas as pd

# FUNCOES DE BANCO DE DADOS

# funcao para solicitar ao usuario as credenciais de banco de dados
# podera ser usado solicitar as credenciais para uma primeira conexao e para uma nova tentativa de conexao caso a primeira falhe
def sql_conn_input():
    
    SERVER = input("-Informe o servidor: ")
    DATABASE = input("-Informe o database: ")
    UID = input("-Informe o usuário: ")
    PWD = input("-Informe a senha: ")
    
    return SERVER, DATABASE, UID, PWD

# funcao para testar repetidamente a conexao com as credenciais passadas para banco de dados
# verifica se a conexao com o banco de dados nao retorna um erro e caso retorno, solicita novas credenciais
def sql_conn_test(SERVER: str, DATABASE: str, UID: str, PWD: str):
    
    while True:
        
        try:
            print('\nTentando conectar ao banco de dados...')
            sql_conn(SERVER, DATABASE, UID, PWD)
            print('\n✅ Conexão bem sucedida!')
            
            return SERVER, DATABASE, UID, PWD
        
        except pyodbc.OperationalError as e:
            print(f"\n❌ Erro de conexão com o banco de dados: \n{e}\n")
            print(f"- Verifique o servidor e se ele está configurado para permitir conexões remotas.\n- Verifique o database informado.\n- Verifique as credenciais passadas (usuário e senha).")
            print(f"\nIniciando nova coleta de dados para nova tentativa: ")
            SERVER, DATABASE, UID, PWD = sql_conn_input()
            
        except pyodbc.Error as e:
            print(f"\n❌ Erro de conexão com o banco de dados: \n{e}\n")
            print(f"- Verifique o servidor e se ele está configurado para permitir conexões remotas.\n- Verifique o database informado.\n- Verifique as credenciais passadas (usuário e senha).")
            print(f"\nIniciando nova coleta de dados para nova tentativa: ")
            SERVER, DATABASE, UID, PWD = sql_conn_input()

# funcao para realizar conexao com banco de dados, so sera feita a conexao quando tiver certeza que os dados estao corretos
def sql_conn(SERVER, DATABASE, UID, PWD):
    
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={SERVER};'
        f'DATABASE={DATABASE};'
        f'UID={UID};'
        f'PWD={PWD}'
    )

    return conn

# FUNCOES DE QUERY

# funcao para que o usuer possa inserir a query que sera executada no baco de dados para retornar as chaves que serao baixadas
def query_writer():
    
    query = input("Digite a QUERY a ser executada no banco de dados (a primeira coluna retornada pela query deve ser referente às chaves de acesso): \n")
    
    return query

# funcao para testar a query passada pelo user
# verifica repetidamente se a query passada pelo user nao retorna um erro do banco de dados e caso retorne, solicita uma nova query
def sql_query_test(conn, query):
    
    #logging.info("Iniciando validação da query.")
    print('\nIniciando validação da query...')
    
    while True:
        
        try:
            query_test = pd.read_sql(query, conn)
            print('\n✅ Query validada!')
            
            return query
        
        except pyodbc.ProgrammingError as e:
            print(f"\n❌ Erro na execução do código SQL: \n{e}\n")
            print(f"- Verifique a integridade e funcionamento da query.")
            
            query = query_writer()
            
        except Exception as e:
            print(f"\n❌ Um erro inesperado ocorreu: \n{e}\n")
            print("- Verifique a integridade e funcionamento da query.")
            
            query = query_writer()