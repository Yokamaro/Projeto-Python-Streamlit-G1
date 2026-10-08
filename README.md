# 🚗 Acidentes de Trânsito no Brasil

Projeto G1 — Linguagem de Programação: Análise e Visualização de Dados com Python.
Aluno: Yago Amaro Zamborlini
Professor: Alexandre Louzada

## Tema

Análise de acidentes de trânsito no Brasil entre 2015 e 2024.

## Objetivo

Investigar padrões temporais, geográficos e relacionados às características dos acidentes, analisando regiões, estados, cidades, tipos de acidente, período do dia, gravidade, feridos, mortes, chuva e visibilidade.

## Base de dados

Arquivo:

`dados/simulacao_acidentes_transito_brasil.csv`

A base utilizada possui 4.440 registros e 15 colunas:

- ano
- mes
- data
- regiao
- uf
- cidade
- tipo_acidente
- periodo_dia
- acidentes
- feridos
- mortes
- chuva_mm
- visibilidade
- veiculos_envolvidos
- nivel_gravidade

## Tecnologias obrigatórias

- Python
- Pandas
- Matplotlib
- Seaborn
- Streamlit
- GitHub

## Funcionalidades intermediárias

O dashboard possui:

- filtros múltiplos;
- KPIs dinâmicos;
- análise temporal;
- dashboards organizados em seções;
- visualizações comparativas;
- tabela detalhada;
- análise de gravidade;
- análise climática.

## Funcionalidades avançadas escolhidas

### 1. Séries temporais avançadas

Foi utilizada uma série temporal mensal com média móvel de três meses para observar tendências e suavizar oscilações.

### 2. Correlação estatística

Foi criada uma matriz de correlação entre:

- acidentes;
- feridos;
- mortes;
- chuva em milímetros;
- veículos envolvidos.

## Estrutura

```text
projeto-acidentes-transito/
│
├── app.py
├── requirements.txt
├── README.md
├── index.html
├── dados/
│   └── simulacao_acidentes_transito_brasil.csv
├── database/
├── notebooks/
│   └── analise_acidentes.ipynb
└── imagens/
```

## Como executar

No terminal:

```bash
pip install -r requirements.txt
```

Depois:

```bash
streamlit run app.py
```

## Publicação

O projeto está preparado para:

- GitHub — código-fonte;
- GitHub Pages — página de apresentação;
- Streamlit Community Cloud — dashboard.

## Observação

Os desafios opcionais não foram implementados, conforme solicitado.
