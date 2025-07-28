import os
import zipfile

# funcao que define e cria os diretorios e pastas que serao utilizados durante a extracao
def create_path():
    
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    extracao_xml = os.path.join(downloads_path, "Extracao_XML")

    folder1 = os.path.join(extracao_xml, "Download_XML_1")
    os.makedirs(folder1, exist_ok=True)

    temp_folder = os.path.join(extracao_xml, f"Temp_Download")
    os.makedirs(temp_folder, exist_ok=True)

    zip_path = os.path.join(extracao_xml, "Download_Evento")
    os.makedirs(zip_path, exist_ok=True)

    temp_zip_path = os.path.join(extracao_xml, "Temp_Download_Evento")
    os.makedirs(temp_zip_path, exist_ok=True)

    return extracao_xml, temp_folder, zip_path, temp_zip_path

# funcao que verifica quais chaves ja existem na pasta Extracao_XML
# serve para recomecar a extracao sem precisar baixar chaves novamente
def list_existing_files(path):
    
    existing_files = []
    
    for folder in os.listdir(path):
        full_folder = os.path.join(path, folder)
        
        if os.path.isdir(full_folder):
            existing_files.extend(
                file.split(".")[0] 
                for file in os.listdir(full_folder) 
                if file.endswith(".xml") or file.endswith(".zip")
        )
            
    return set(existing_files)

# funcao que cria um arquivo .txt para armazenar as chaves que nao foram baixadas
def error_txt(chaves_erro):
    
    modo = "a" if os.path.exists(os.path.join(os.path.join(os.path.expanduser("~"), "Downloads"), "chaves_erro.txt")) else "w"
    with open(os.path.join(os.path.join(os.path.expanduser("~"), "Downloads"), "chaves_erro.txt"), modo, encoding="utf-8") as arquivo:
        for i in chaves_erro:
            arquivo.write(f'{i}\n')

# funcao que extrai os xmls que possuem eventos vinculados (sao baixados como .zip)
def zip_extract(temp_zip_path, zip_path, zip_file):
    
    zip_full_path = os.path.join(temp_zip_path, zip_file)
    
    with zipfile.ZipFile(zip_full_path, 'r') as zip_ref:
        zip_ref.extractall(zip_path)

# funcao que compacta as pastas no final da extracao
def compress_files(extracao_xml, zip_name="Extracao_XML.zip"):
    
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    zip_path = os.path.join(downloads_path, zip_name)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(extracao_xml):
            for file in files:
                if file.endswith(".xml"):
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, arcname=os.path.relpath(file_path, extracao_xml))
                    
    print(f"✅ Arquivos compactados em: {zip_path}")
