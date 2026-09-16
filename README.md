# GameTracker

Projeto de portfólio em desenvolvimento: uma plataforma para catalogar jogos automaticamente a partir de uma API pública de dados de games (IGDB), com normalização dos dados, armazenamento em banco relacional, exposição via API REST e exportação para Excel.

## Status

🚧 Em desenvolvimento — construído em etapas incrementais e documentadas.

## Funcionalidades implementadas até agora

- Autenticação com a IGDB via OAuth2 (fluxo client credentials).
- Busca de uma lista de jogos, com relatório separado dos que não foram encontrados.
- Resolução de ambiguidade em três camadas, para lidar com inconsistências reais da base de dados da IGDB (que é colaborativa e por isso nem sempre categoriza corretamente):
  1. Filtra por categoria (`main_game`), descartando DLCs, expansões e bundles.
  2. Filtra por palavras-chave no nome (remaster, edition, goty, etc.), para pegar edições especiais mal categorizadas.
  3. Entre os candidatos restantes, escolhe o nome com maior similaridade textual ao termo buscado, em vez de confiar na ordem de relevância da própria API.

## Tecnologias

- Python
- Requests
- python-dotenv

*(a lista cresce conforme o projeto avança: PostgreSQL, SQLAlchemy, FastAPI, Docker, Pytest, GitHub Actions)*

## Estrutura do projeto

app/
├── core/ # configuração (leitura de variáveis de ambiente)
├── integrations/ # cliente da IGDB (autenticação + busca)
├── services/ # regras de negócio (coleta em lote de jogos)
└── main.py # ponto de entrada


## Como rodar

1. Clone o repositório.
2. Crie um ambiente virtual: `python -m venv venv`
3. Ative o ambiente virtual.
4. Instale as dependências: `pip install -r requirements.txt`
5. Crie um arquivo `.env` na raiz com:

IGDB_CLIENT_ID=seu_client_id
IGDB_CLIENT_SECRET=seu_client_secret

   (veja como obter essas credenciais na seção abaixo)
6. Rode: `python -m app.main`

## Como obter credenciais da IGDB

1. Crie uma conta em [dev.twitch.tv](https://dev.twitch.tv/).
2. Registre uma aplicação em "Your Console" → "Applications".
3. Gere um Client Secret na página da aplicação.
4. Use o Client ID e Client Secret gerados no `.env`.

## Roadmap

- [x] v0.1 — Consulta de um jogo na IGDB
- [x] v0.2 — Coleta de uma lista de jogos e resolução de ambiguidade
- [ ] v0.3 — Armazenamento em PostgreSQL
- [ ] v0.4 — Exportação para Excel
- [ ] v0.5 — API REST com FastAPI
- [ ] v0.6 — Interface web
- [ ] v0.7 — Docker
- [ ] v0.8 — Testes automatizados
- [ ] v0.9 — CI/CD com GitHub Actions
- [ ] v1.0 — Documentação final