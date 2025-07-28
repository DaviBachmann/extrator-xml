import os
import pyodbc
import requests
import warnings
import threading
from queue import Queue
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

from features.api import def_url
from features.extraction import extract, file_writer
from features.operations import create_path, list_existing_files, zip_extract, compress_files, error_txt
from features.input_handler import get_cliente, get_produto, get_tipo, get_retorno_chaves

from core.utils import limpa_tela

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

# FUNCAO PRINCIPAL

def main():
    
    # Funcao principal que chama as outras funcoes para realizar a extracao
    
    limpa_tela()
    print('Bem-vindo ao extrator de XMLs!')
    
    cliente = get_cliente()
    print(f'-> {cliente if cliente in ["SaaS", "Carrefour", "DHL", "Riachuelo"] else "Definido manualmente pelo usuário"}')
    
    produto = get_produto()
    print(f'-> {produto}')
        
    tipo = get_tipo()
    print(f'-> {"Emissão" if tipo == "Emissao" else tipo}')
        
    url = def_url(cliente, produto, tipo) if cliente in ['SaaS', 'Carrefour', 'DHL', 'Riachuelo'] else cliente
    
    limpa_tela()
        
    print(
    f"""
                Baixar XML
============================================
              Escolhas de URL
|Cliente: {cliente if cliente in ['SaaS', 'Carrefour', 'DHL', 'Riachuelo'] else 'Definido manualmente pelo usuário'}
|Produto: {produto}
|Tipo: {"Emissão" if tipo == "Emissao" else tipo}
|URL: {url}
============================================""")
    
    retorno_chaves = get_retorno_chaves()
    
    chaves, SERVER, DATABASE, UID = retorno_chaves.get('chaves'), retorno_chaves.get('servidor'), retorno_chaves.get('database'), retorno_chaves.get('usuario')
    
    extracao_xml, temp_folder, zip_path, temp_zip_path = create_path() # log_path
    chaves_erro = []
    lock = threading.Lock()
    queue = Queue()
 
    print('\nVerificando arquivos existentes...')
    existing_files = list_existing_files(extracao_xml)
    conjunto_chaves = set(chaves)
    chaves_novas = conjunto_chaves - existing_files
    
    if len(existing_files) > 0:
        
        print(f"\n{len(existing_files)} chaves já estão baixadas!")

    if len(chaves_novas) == 0:
        
        print(f"\n✅ Todas as chaves coletadas na query ou inserção já estão baixadas!")
        input("\nPressione ENTER para sair!")
    else:
        
        limpa_tela()
    
    if retorno_chaves.get('servidor') is not None:
        print(
        f"""
                Baixar XML
============================================
              Escolhas de URL
|Cliente: {cliente if cliente in ['SaaS', 'Carrefour', 'DHL', 'Riachuelo'] else 'Definido manualmente pelo usuário'}
|Produto: {produto}
|Tipo: {"Emissão" if tipo == "Emissao" else tipo}
|URL: {url}
============================================""")
        
        print(
        f"""
============================================
          Configurações de Banco
|Servidor: {SERVER}
|Database: {DATABASE}
|Usuário: {UID}
============================================""")
    else:
        print(
        f"""
============================================
              Escolhas de URL
|Cliente: {cliente if cliente in ['SaaS', 'Carrefour', 'DHL', 'Riachuelo'] else 'Definido manualmente pelo usuário'}
|Produto: {produto}
|Tipo: {"Emissão" if tipo == "Emissao" else tipo}
|URL: {url}
============================================""")
        
    print('\nIniciando extração dos arquivos restantes...')
    workers = os.cpu_count() or 5
        
    with ThreadPoolExecutor(max_workers=workers) as executor:
            
        futures = [
            executor.submit(extract, idx, chave, extracao_xml, temp_folder, temp_zip_path, cliente, produto, tipo, chaves_erro, lock)
                for idx, chave in enumerate(chaves_novas)
        ]
        for _ in tqdm(as_completed(futures), total=len(chaves_novas), desc="Progresso", unit="arquivo", ncols=80):
            pass
    
    events_files = len(os.listdir(temp_zip_path))
    if events_files > 0:
        print(f"\n{events_files} arquivos foram identificados com eventos vinculados. Iniciando a extração dos arquivos com eventos vinculados...")
    else:
        print('Não foram identificados arquivos com eventos vinculados.')
        
    for zip_file in os.listdir(temp_zip_path):
        if zip_file.endswith('.zip'):
            zip_extract(temp_zip_path, zip_path, zip_file)
        
    print('\n✅ Coletânea de XMLs finalizada!')
            
    print(f'\n✅ {len(chaves)-len(chaves_erro)} arquivos foram baixados!\n❌ {len(chaves_erro)} encontraram algum erro e não puderam ser baixados!')
    file_writer(extracao_xml, temp_folder, "Download_XML_1")
    
    print("\nCompactando arquivos...")
    compress_files(extracao_xml)

    if len(chaves_erro) > 0:
        error_txt(chaves_erro)
        print(f"\n✅ Arquivo de chaves faltantes criado com {len(chaves_erro)} chaves em Downloads\\chaves_erro.txt!")
        
    input('\nPressione ENTER para sair!')

try:
    if __name__ == "__main__":
        main()
except KeyboardInterrupt:
    print("\n\nPrograma encerrado pelo usuário.")
    input('Pressione ENTER para sair!')
except pyodbc.Error as e:
    print(f"\n\n❌ Erro no banco de dados: {e}")
    print("Certifique-se de que o servidor e as credenciais estão corretos.")
    input('Pressione ENTER para sair!')
except Exception as e:
    print(f"\n\n❌ Um erro inesperado ocorreu: {e}")
    input('Pressione ENTER para sair!')