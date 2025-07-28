import time
import shutil
import os
from features.api import def_url, content_type, api_get

# FUNCOES DIRETAMENTE RELACIONADAS A EXTRACAO DOS XMLs

# funcao que processa a chave, ela apenas coloca um valor na queue para que o ThreadPoolExecutor saiba que a chave foi processada
def process_chave(chave, queue):
    
    time.sleep(0.1)
    queue.put(1)
    
    return f"Processed {chave}"

# funcao que escreve os arquivos em uma pasta temporaria
# ela realiza uma verificao na quantiade de arquivos da pasta temporaria, caso atinja o limite, ela envia os arquivos para uma pasta definitiva
def temp_file_writer(extracao_xml, temp_zip_path, temp_folder, idx, chave, conteudo, extensao):
    
    if extensao == ".xml":
        file_path = os.path.join(temp_folder, f"{chave}{extensao}")
        
        with open(file_path, 'wb') as file:
            file.write(conteudo)
            
        if len(os.listdir(temp_folder)) >= 5000:
            create_folder_xml(extracao_xml, temp_folder, idx)
            
    elif extensao == ".zip":
        file_path = os.path.join(temp_zip_path, f"{chave}{extensao}")
        
        with open(file_path, 'wb') as file:
            file.write(conteudo)
            
# funcao responsavel por definir e criar as respectivas pastas que armazenam os xmls de acordo com o 'id' da chave
# a cada 100.000 chaves, uma nova pasta e criada para que nao haja sobrecarga de escrita no disco
def create_folder_xml(extracao_xml, temp_folder, idx):
    
    num_folder = int(idx/100000) + 1
    path = os.path.join(extracao_xml, f"Download_XML_{num_folder}")
    os.makedirs(path, exist_ok=True)

    file_writer(extracao_xml, temp_folder, path)

# funcao responsavel por passar os arquivos da pasta temporaria para a pasta definitiva de xml
def file_writer(extracao_xml, temp_folder, path):
    
    for arquivo in os.listdir(temp_folder):
        
        caminho_origem = os.path.join(temp_folder, arquivo)
        caminho_dest = os.path.join(os.path.join(extracao_xml, path), arquivo)
        shutil.move(caminho_origem, caminho_dest)
        
# funcao principal para realizar a extracao, ela chama as outras funcoes sub-principais para baixar cada xml
def extract(idx, chave, extracao_xml, temp_folder, temp_zip_path, cliente, produto, tipo, chaves_erro, lock=None):
    
    url = (def_url(cliente, produto, tipo)) + chave
    conteudo, conteudo_type = api_get(url)
    extensao = content_type(conteudo_type)
    
    if conteudo is not None:
        temp_file_writer(extracao_xml, temp_zip_path, temp_folder, idx, chave, conteudo, extensao)
    
    else:
        if lock:
            with lock:
                return chaves_erro.append(chave)
        else:
            return chaves_erro.append(chave)