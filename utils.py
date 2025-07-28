import os
import urllib.request

# FUNCOES AUXILIARES E DE UTILIDADES

def limpa_tela():
    _ = os.system('cls' if os.name == 'nt' else 'clear')

def menu(
    opcoes: dict, 
    mensagem: str = None
):
    if mensagem:
        print(mensagem)
    escolha = input('>> ')
    
    while True:
        if escolha in opcoes:
            
            if opcoes[escolha] == 'Outro':
                return input(': ')
            
            if callable(opcoes[escolha]):
                return opcoes[escolha]()
            
            else:
                return opcoes[escolha]
            
        else:
            escolha = input(f'Escolha inválida ({escolha}). Por favor, informe novamente: ')

def verificar_conexao():
    try:
        urllib.request.urlopen('https://www.google.com', timeout=5)
        return True
    except:
        return False