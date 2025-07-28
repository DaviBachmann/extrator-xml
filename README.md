# 📁 Extrator de XML

Projeto em Python para download massivo de documentos XML utilizando **multithreading**, **API** e **banco de dados**. Criado para acelerar extrações que antes levavam horas, agora com performance otimizada e múltiplas formas de input.

---

## 📌 Descrição Geral

Esse projeto foi desenvolvido para **automatizar e otimizar** o processo de download de documentos fiscais eletrônicos (XMLs) na minha empresa atual. Utilizando requisições simultâneas via threads, ele realiza **"gets" em massa** a partir de uma API definida pelo usuário, com base nas **chaves de acesso coletadas** de diversas formas.

---

## ⚙️ Funcionalidades

- ✅ Interface via terminal para configuração rápida
- 🌐 Coleta de chaves por:
  - Input manual
  - Query em banco de dados (SQL Server)
  - Arquivo `.txt`
- 🧠 Verificação de quais XMLs já foram baixados (evita duplicidade)
- 🗃️ Organização automática em pastas por quantidade de documentos
- ⚡ Download massivo com threads simultâneos
- 📦 Pós-processamento:
  - Extração de arquivos `.zip`
  - Compressão final para entrega
- 🔁 Retomada automática de extrações pausadas

---

## 💡 Motivação do Projeto

O projeto nasceu de um cenário real: a necessidade frequente de baixar milhares de XMLs para atendimento de demandas de clientes. Antes, o processo era feito manualmente via PowerShell, com desempenho limitado (~10 mil/hora).  

Com esse extrator, o tempo caiu drasticamente, chegando a cerca de **100 mil documentos/hora**, dependendo do hardware e estabilidade da rede.

---

## 🚀 Exemplo de Uso Real

**Cenário:**  
Cliente *Riachuelo* solicita extração de documentos NFCe:

- **Período:** 01/01/2025 a 31/01/2025  
- **Status dos documentos:** 6  

### 🧭 Etapas de Execução

1. **Definir URL da API**  
   Selecione:
   - Cliente: Riachuelo
   - Produto: NFCe
   - Tipo de documento: 65

2. **Escolher método de coleta das chaves**
   - Manual (copiar e colar)
   - Banco de dados (inserir credenciais e query)
   - Arquivo `.txt`

3. **Iniciar download dos documentos**  
   O programa organiza, divide em pastas temporárias e evita repetição.

4. **Reiniciar extrações interrompidas**  
   O extrator verifica automaticamente quais documentos já foram baixados no diretório `../Extracao_XML` e ignora os repetidos.

---

> Projeto criado por [Davi Bachmann](https://github.com/DaviBachmann) — Cientista de Dados em formação, com foco em automação, dados e performance.
