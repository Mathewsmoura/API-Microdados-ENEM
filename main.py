from fastapi import FastAPI
import pandas as pd
import json

app = FastAPI(
    title="API Microdados Enem",
    description="Modelo de API para consumir dados sobre o exame nacional do ensino médio.",
    version="1.0.0",
)

#Carregar os dados do CSV
try:
    #Usar um caminho relativo ou absoluto conforme necessário
    enem_data = pd.read_csv('caminho/do/arquivo.csv')
except FileNotFoundError:
    enem_data = pd.DataFrame() #DF vazuio em caso de erro
    
    @app.get("/")
    def home():
        return {"message": "Bem-vindo à API de Microdados Enem! Acesse /docs para a documentação interativa."}
    
    @app.get("/dados_gerais")
    def get_dados_gerais():
        """Retorna uma visão geral dos dados do Enem.
        """
        if enem_data.empty:
            return {"error": "Dados não carregados. Verifique o caminho do arquivo."}
        
        # Exemplo: Retorna os 5 primeiros registros
        return json.loads(enem_data.head().to_json(orient="records"))
    
    @app.get("/dados_por_estado/{estado}")
    def get_dados_por_estado(estado: str):
        """
        Filtra e retornar dados do ENEM por estado.
        """
        if enem_data.empty:
            return {"error": "Dados não carregados."}
        
        # Exemplo: filtra os dados para um estado especifico.
        dados_filtrados = enem_data[enem_data['SG_UF_RESIDENCIA'] == estado.upper()]
        
        if dados_filtrados.empty:
            return {"error": f"Nenhum dado encontrado para o estado: {estado}."}

        return json.loads(dados_filtrados.head().to_json(orient="records"))
