from fastapi import FastAPI, HTTPException
import pandas as pd
import json

app = FastAPI(
    title="API Microdados Enem",
    description="Modelo de API para consumir dados sobre o exame nacional do ensino médio.",
    version="1.0.1",
)

#Carregar os dados do CSV
try:
    #Usar um caminho relativo ou absoluto conforme necessário
    enem_data = pd.read_csv('caminho/do/arquivo.csv')
    
    #Padronização dos tipos de coluna (se necessário)
    colunas_notas = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
    for col in colunas_notas:
        enem_data[col]  = pd.to_numeric(enem_data[col], errors='coerce')
        
        enem_data.dropna(subset=colunas_notas, inplace=True)
        
except FileNotFoundError:
    enem_data = pd.DataFrame() #DF vazio em caso de erro
    
    @app.get("/")
    def home():
        return {"message": "Bem-vindo à API de Microdados Enem! Acesse /docs para a documentação interativa."}
    
    @app.get("/dados_gerais")
    def get_dados_gerais(ano: int = None):
        """ 
        Retorna uma amostra dos primeiros 5 registros gerais do ENEM, com filtro opcional por ano.
        """
        if enem_data.empty:
            raise HTTPException(status_code=404, detail="Dados não carregados. Verifique o caminho do arquivo.")

        if ano is not None:
            dados_filtrados = enem_data[enem_data["NU_ANO"] == ano]
            if dados_filtrados.empty:
                raise HTTPException(status_code=404, detail=f"Nenhum dado encontrado para o ano {ano}.")
            return json.loads(dados_filtrados.head(5).to_json(orient="records"))

        return json.loads(enem_data.head(5).to_json(orient="records"))
    
    @app.get("/dados_por_estado/{estado}")
    def get_dados_por_estado(estado: str):
        """
        Retorna uma amostra dos primeiros 5 registros do ENEM para um estado específico.
        """
        if enem_data.empty:
            raise HTTPException(status_code=404, detail="Dados não carregados. Verifique o caminho do arquivo.")

        dados_filtrados = enem_data[enem_data["SG_UF_RESIDENCIA"] == estado.upper()]

        if dados_filtrados.empty:
            raise HTTPException(status_code=404, detail=f"Nenhum dado encontrado para o estado '{estado}'.")

        return json.loads(dados_filtrados.head(5).to_json(orient="records"))

### Novas Rotas de Análise e Consulta

@app.get("/participantes")
def get_participantes_com_filtros(
    idade: int = None,
    sexo: str = None,
    cor: str = None,
    escola: str = None,
    uf: str = None,
    min_nota_mt: float = None,
    max_nota_mt: float = None,
    limit: int = 10
):
    """
    Consulta participantes com filtros avançados.
    
    - **idade**: Filtra por idade do participante.
    - **sexo**: Filtra por sexo (M ou F).
    - **cor**: Filtra por cor/raça (e.g., BRANCA, PRETA, PARDA).
    - **escola**: Filtra pelo tipo de escola (e.g., PUBLICA, PRIVADA).
    - **uf**: Filtra pela UF de residência.
    - **min_nota_mt**: Filtra pela nota mínima em Matemática.
    - **max_nota_mt**: Filtra pela nota máxima em Matemática.
    - **limit**: Limita o número de resultados (padrão: 10).
    """
    if enem_data.empty:
        raise HTTPException(status_code=404, detail="Dados não carregados.")
    
    df_filtrado = enem_data.copy()
    
    filtros = [
        ('NU_IDADE', idade), ('TP_SEXO', sexo.upper() if sexo else None),
        ('SG_UF_RESIDENCIA', uf.upper() if uf else None)
    ]
    
    for coluna, valor in filtros:
        if valor is not None:
            df_filtrado = df_filtrado[df_filtrado[coluna] == valor]
    
    # Mapeamentos para filtros categóricos
    mapeamentos = {
        'cor': {'BRANCA': 1, 'PRETA': 2, 'PARDA': 3, 'AMARELA': 4, 'INDIGENA': 5},
        'escola': {'PUBLICA': 2, 'PRIVADA': 3}
    }
    
    if cor and cor.upper() in mapeamentos['cor']:
        df_filtrado = df_filtrado[df_filtrado['TP_COR_RACA'] == mapeamentos['cor'][cor.upper()]]
    
    if escola and escola.upper() in mapeamentos['escola']:
        df_filtrado = df_filtrado[df_filtrado['TP_ESCOLA'] == mapeamentos['escola'][escola.upper()]]

    # Filtros de faixa de nota
    if min_nota_mt is not None:
        df_filtrado = df_filtrado[df_filtrado['NU_NOTA_MT'] >= min_nota_mt]
    if max_nota_mt is not None:
        df_filtrado = df_filtrado[df_filtrado['NU_NOTA_MT'] <= max_nota_mt]

    if df_filtrado.empty:
        raise HTTPException(status_code=404, detail="Nenhum participante encontrado com os filtros aplicados.")
    
    resultados = df_filtrado.head(limit)
    return json.loads(resultados.to_json(orient="records"))

@app.get("/estatisticas_agregadas")
def get_estatisticas_agregadas():
    """
    Retorna estatísticas agregadas (médias, medianas e desvios padrão) das notas.
    """
    if enem_data.empty:
        raise HTTPException(status_code=404, detail="Dados não carregados.")
        
    estatisticas = enem_data[['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']].agg(['mean', 'median', 'std']).to_dict()
    
    return estatisticas

@app.get("/distribuicao_demografica/{caracteristica}")
def get_distribuicao_demografica(caracteristica: str):
    """
    Retorna a contagem de participantes por uma característica demográfica.
    
    - **característica**: Coluna para a análise (e.g., 'SG_UF_RESIDENCIA', 'TP_SEXO', 'TP_COR_RACA', 'NU_IDADE').
    """
    if enem_data.empty:
        raise HTTPException(status_code=404, detail="Dados não carregados.")
        
    if caracteristica not in enem_data.columns:
        raise HTTPException(status_code=400, detail=f"Característica '{caracteristica}' não encontrada nos dados.")
        
    distribuicao = enem_data[caracteristica].value_counts().to_dict()
    
    return distribuicao

@app.get("/ranking_por_uf")
def get_ranking_por_uf():
    """
    Retorna o ranking de médias de notas de Matemática por UF.
    """
    if enem_data.empty:
        raise HTTPException(status_code=404, detail="Dados não carregados.")
        
    ranking = enem_data.groupby('SG_UF_RESIDENCIA')['NU_NOTA_MT'].mean().sort_values(ascending=False).to_dict()
    
    return ranking
