# API de Análise dos Microdados do ENEM

![Versão](https://img.shields.io/badge/versão-1.0.2-blue)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green?logo=fastapi)

Uma API RESTful desenvolvida para servir e analisar os dados do Exame Nacional do Ensino Médio (ENEM). O projeto permite realizar consultas, filtros e agregações estatísticas sobre o desempenho e perfil demográfico dos participantes.

## 📋 Sobre o Projeto

O objetivo desta API é fornecer uma interface rápida e eficiente para explorar o grande volume de dados dos Microdados do ENEM. Em vez de manipular arquivos CSV de vários gigabytes diretamente, esta API pré-processa e carrega os dados em memória, expondo endpoints otimizados para análises comuns, como:

-   Filtragem de participantes por critérios demográficos e de notas.
-   Cálculo de estatísticas agregadas (médias, medianas).
-   Geração de rankings e distribuições.

## ✨ Principais Funcionalidades

-   **Pré-processamento de Dados:** Limpeza e otimização dos dados no momento do carregamento para garantir performance e consistência.
-   **Filtros Avançados:** Endpoint `/participantes` que permite combinar múltiplos filtros (idade, sexo, UF, notas, etc.).
-   **Análises Estatísticas:** Endpoint `/estatisticas_agregadas` para obter médias, medianas e desvios padrão das notas.
-   **Análise Demográfica:** Endpoint dinâmico `/distribuicao_demografica/{caracteristica}` para contagem de participantes por UF, sexo, cor/raça, etc.
-   **Ranking por UF:** Endpoint `/ranking_por_uf` que calcula e ordena a média de notas por estado.
-   **Tratamento de Erros:** Uso de `HTTPException` para fornecer feedback claro e códigos de status HTTP corretos.

## 🛠️ Tecnologias Utilizadas

-   **[Python](https://www.python.org/)**: Linguagem de programação principal.
-   **[FastAPI](https://fastapi.tiangolo.com/)**: Framework web de alta performance para a construção da API.
-   **[Pandas](https://pandas.pydata.org/)**: Biblioteca para manipulação e análise dos dados.
-   **[Uvicorn](https://www.uvicorn.org/)**: Servidor ASGI para executar a aplicação FastAPI.

## 🚀 Como Executar

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Linux / macOS
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure o arquivo de dados:**
    -   Faça o download do arquivo de microdados do ENEM.
    -   No arquivo `main.py`, altere a linha `enem_data = pd.read_csv('caminho/do/arquivo.csv', ...)` para o caminho correto do seu arquivo.

5.  **Inicie o servidor:**
    ```bash
    uvicorn main:app --reload
    ```

6.  **Acesse a documentação interativa:**
    Abra seu navegador e acesse [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## 🔮 Próximos Passos

-   [ ] Integrar um banco de dados (ex: PostgreSQL, SQLite) para evitar o carregamento do CSV em memória.
-   [ ] Utilizar variáveis de ambiente para configurar o caminho do arquivo de dados.
-   [ ] Adicionar paginação aos resultados.
-   [ ] Criar testes automatizados para os endpoints.

Obs: Ao decorrer do desenvolvimento, incluiremos novas documentações.