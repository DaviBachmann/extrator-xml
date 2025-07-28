from core.utils import menu
from features.api import url_manual
from features.keys import by_insert, by_sql, by_txt

def get_operacao():
    operacao = menu(
    {
        '1':'xml',
        '2':'pdf'
    },
    """
===========================================
                 Operação:
|1 - Baixar XML
|2 - Baixar PDF
==========================================="""
    )
    return operacao

def get_cliente():
    cliente = menu(
    {
        '1':'SaaS',
        '2':'Carrefour',
        '3':'DHL',
        '4':'Riachuelo',
        '5':url_manual
    },
    """
===========================================
                 Cliente:
|1 - SaaS
|2 - Carrefour
|3 - DHL
|4 - Riachuelo
|5 - Outro (Inserir URL completa manualmente)
==========================================="""
    )
    return cliente

def get_produto():
    produto = menu(
    {
        '1':'NFe',
        '2':'CTe',
        '3':'NFCe',
        '4':'Outro'
    },
    """
===========================================
                 Produto:
|1 - NFe
|2 - CTe
|3 - NFCe
|4 - Outro (Apenas se o cliente foi definido manualmente)
===========================================""")
    return produto

def get_tipo():
    tipo = menu(
    {
        '1':'Emissao',
        '2':'Recebimento'
    },
    """
===========================================
          Emissão ou Recebimento:
|1 - Emissão
|2 - Recebimento
===========================================""")
    return tipo

def get_retorno_chaves():
    retorno_chaves = menu(
    {
        '1':by_insert,
        '2':by_sql,
        '3':by_txt
    },
    """
===========================================
   Opções de coleta de chaves de acesso:
|1 - Inserir chaves
|2 - Coletar chaves via banco de dados
|3 - Coletar chaves via arquivo .txt
===========================================""")
    return retorno_chaves