# API MICRODADOS ENEM

- Modelo de API para consumir dados sobre o exame nacional do ensino médio.

# - Versão 1.0.1

1 - Pré-processamento de Dados: No primeiro código, os dados eram carregados "brutos". Agora, incluímos um passo de pré-processamento dentro do bloco try...except. Isso garante que as colunas de notas sejam tratadas como números e que linhas com notas ausentes sejam removidas (.dropna()). Isso é crucial para as análises estatísticas.

2 - Adição de Novas Rotas: As principais mudanças são as novas rotas, que atendem aos requisitos de análise que você solicitou:
•	/estatisticas_agregadas: Utiliza o .agg() do Pandas para calcular médias, medianas e desvios padrão de todas as notas de uma vez, devolvendo um resumo estatístico em uma única chamada.
•	/distribuicao_demografica/{caracteristica}: Uma rota dinâmica que usa value_counts() do Pandas para contar a frequência de valores em uma coluna, permitindo analisar a distribuição de participantes por qualquer característica demográfica que você passar como parâmetro de rota.
•	/ranking_por_uf: Calcula a média de notas de Matemática por estado (.groupby('SG_UF_RESIDENCIA')) e as ordena, gerando um ranking.
3 - Melhoria na Rota de Filtros (/participantes): A lógica de filtragem foi refatorada. Ao invés de usar ifs separados para cada tipo de filtro, agrupamos alguns deles em um loop para um código mais limpo. Além disso, adicionamos um dicionário de mapeamento para tratar as colunas de cor e tipo de escola, que usam códigos numéricos no dataset do ENEM, mas que são mais fáceis de filtrar usando seus nomes (por exemplo, PUBLICA em vez de 2).

4 - Tratamento de Erros com HTTPException: Em vez de apenas retornar um dicionário de erro ({"error": "..."}), as novas rotas usam raise HTTPException. Essa é a maneira recomendada pelo FastAPI para lidar com erros, pois ela envia o código de status HTTP correto (como 404 Not Found ou 400 Bad Request), facilitando o tratamento de erros para quem consome a API.

Obs: Ao decorrer do desenvolvimento, incluiremos novas documentações.