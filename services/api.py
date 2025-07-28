import requests

# FUNCOES RELACIONADAS A API

# funcao que define qual a url que fara o get para baixar o xml de acordo com o que o user definir pois cada cliente possui um endpoint diferente
def def_url(cliente, produto, tipo):
    
    lista_url = {
        
        "SaaS":{
            "NFe":f"https://saas.inventti.app/nfe/api/XML/XML{tipo}?chave=",
            "CTe":f"http://saas.inventti.app/CTePackMonitor/XML.aspx/Xml{tipo}?chaveCTe=",
            "NFCe":f"https://saas.inventti.app/nfce/api/XML/XML{tipo}?chave="
        },
        
        "Carrefour":{
            "NFCe":f"http://10.113.132.1/nfcepackwebappoa/api/XML/XML{tipo}?chave=",
            "NFe":f"http://carrefour.inventti.app/nfepackwebapp/api/XML/XML{tipo}?chave=",
            "NFeBalcao":f"http://10.113.132.244/NFePackWebAppOABalcao/api/XML/XML{tipo}?chave=",
            "NFeCD":f"http://10.113.132.245/NFePackWebAppCDs/api/XML/XML{tipo}?chave="
        },
        
        "DHL":{
            "CTe":f"https://saas.inventti.app/CTePackMonitorDHL/XML.aspx/Xml{tipo}?chaveCTe="
        },
        
        "Riachuelo":{
            "NFCe":f"https://riachuelo.inventti.app/nfce/api/XML/XML{tipo}?chave="
        }
    }

    if cliente in lista_url:
            return lista_url[cliente][produto]
    else:
        return cliente

# funcao que permite o user inserir a url manualmente
def url_manual():
    return input("""
Informe a URL completa
Exemplo: https://Dominio/NomeWebService/api/XML/XMLTipo?chave=

Dominio: Dominio do servidor (saas.inventti.app; localhost; etc)
NomeWebService: Nome do webservice instalado (nfe; NFePack; etc)
XMLTipo: Tipo de XML que deseja baixar (Emissao; Recebimento; etc)

: """)

# funcao que define se o arquivo devera ser baixado como xml ou zip (notas com eventos vinculados devem ser baixadas como zip pois possuem um xml para cada evento)
def content_type(conteudo_type):
    
    types = {
        "application/zip":".zip",
        "application/xml":".xml",
        "text/xml":".xml",
        "application/octet-stream":".xml"
    }

    if conteudo_type in types:
        return types[conteudo_type]

# funcao que realiza o get na api para baixar cada chave
def api_get(url):
    
    try:
        response = requests.get(url, timeout=15, verify=False)
        if response.status_code == 200:
            return response.content, response.headers.get("Content-Type")
        #else:
            #logging.error("Erro na requisição.")
            
    except requests.exceptions.RequestException as e:
        #logging.error(f"Erro ao acessar URL: {url}.")
        return None, None