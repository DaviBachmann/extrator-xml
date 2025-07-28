import pandas as pd
from features.database import sql_conn_input, sql_conn_test, sql_conn, query_writer, sql_query_test

# FUNCOES QUE DEFINEM QUAIS CHAVES SERAO BAIXADAS NA EXTRACAO

# funcao no qual o usuario digita as chaves que serao baixadas
def by_insert():
    
    chaves = input('Insira as chaves de acesso (chaves separadas por vírgula ou espaço e sem aspas): ').replace(',', '').replace("'", "").replace('  ', ' ').strip().split(' ')
    
    return {"chaves": chaves}

# funcao para coletar as chaves via arquivo .txt
def by_txt():
    
    txt_path = input('Insira o caminho completo do arquivo .txt com as chaves de acesso: \n').replace('"', '').replace("'", '').strip()
    
    if txt_path.endswith('.txt'):
        while True:
            try:
                with open(txt_path, 'r') as arquivo:
                    linhas = arquivo.readlines()
                    chaves = [linha.strip() for linha in linhas]
                return {"chaves": chaves}
            
            except FileNotFoundError as e:
                txt_path = input(f'Caminho de arquivo ({txt_path}) não encontrado, insira novamente: \n')
    
    elif txt_path.endswith('.csv'):
        while True:
            try:
                chaves = pd.read_csv(txt_path, sep = " ", header = None)
                chaves = chaves[0].tolist()
                return {"chaves": chaves}
            
            except FileNotFoundError as e:
                txt_path = input(f'Caminho de arquivo ({txt_path}) não encontrado, insira novamente: \n')

# funcao para coletar as chaves via query em banco de dados (esta relacionada as funcoes do arquivo database.py)
def by_sql():
    
    print('\nIniciando coleta de dados para conectar ao banco:')
    
    SERVER, DATABASE, UID, PWD = sql_conn_input()
    SERVER, DATABASE, UID, PWD = sql_conn_test(SERVER, DATABASE, UID, PWD)
    conn = sql_conn(SERVER, DATABASE, UID, PWD)

    query = query_writer()
    query = sql_query_test(conn, query)
    
    chaves = pd.read_sql(query, conn)
    conn.close()
    
    return {"chaves": chaves.iloc[:, 0].tolist(), "servidor": SERVER, "database": DATABASE, "usuario": UID}