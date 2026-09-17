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
- Busca por critérios (ano de lançamento, nota mínima), sem precisar informar um nome específico.
- Persistência dos jogos encontrados em PostgreSQL, com prevenção de duplicação: jogos já existentes (identificados pelo `igdb_id`) são atualizados em vez de duplicados.
- Exportação dos dados do banco para uma planilha Excel (.xlsx) formatada: cabeçalho estilizado, filtros automáticos, congelamento da linha de cabeçalho e quebra de texto na coluna de descrição.

## Tecnologias

- Python
- Requests
- python-dotenv
- SQLAlchemy
- PostgreSQL (via Docker)
- psycopg2-binary
- OpenPyXL

*(a lista cresce conforme o projeto avança: FastAPI, Docker completo da aplicação, Pytest, GitHub Actions)*

## Estrutura do projeto

app/
├── core/ # configuração (variáveis de ambiente) e conexão com o banco
├── integrations/ # cliente da IGDB (autenticação + busca por nome + busca por critérios)
├── services/ # regras de negócio (coleta em lote de jogos)
├── models/ # modelos SQLAlchemy (tabelas do banco)
├── repositories/ # acesso a dados (salvar/atualizar jogos no banco)
├── exporters/ # geração da planilha Excel
└── main.py # ponto de entrada


## Como rodar

1. Clone o repositório.
2. Crie um ambiente virtual: `python -m venv venv`
3. Ative o ambiente virtual.
4. Instale as dependências: `pip install -r requirements.txt`
5. Crie um arquivo `.env` na raiz com:

IGDB_CLIENT_ID=seu_client_id
IGDB_CLIENT_SECRET=seu_client_secret
DATABASE_URL=postgresql://gametracker:gametracker@localhost:5432/gametracker

   (veja como obter as credenciais da IGDB na seção abaixo)
6. Suba o banco de dados: `docker compose up -d`
7. Crie as tabelas: `python create_tables.py`
8. Rode: `python -m app.main`
9. O resultado (busca, persistência e exportação) aparece no terminal, e a planilha é gerada em `output/jogos.xlsx`.

## Como obter credenciais da IGDB

1. Crie uma conta em [dev.twitch.tv](https://dev.twitch.tv/).
2. Registre uma aplicação em "Your Console" → "Applications".
3. Gere um Client Secret na página da aplicação.
4. Use o Client ID e Client Secret gerados no `.env`.

## Banco de dados

O projeto usa PostgreSQL rodando via Docker, com dados persistidos em um volume nomeado (não são perdidos ao reiniciar o container).

Para subir o banco:

docker compose up -d


Para criar as tabelas (primeira vez, ou após alterar os modelos):

python create_tables.py


## Roadmap

- [x] v0.1 — Consulta de um jogo na IGDB
- [x] v0.2 — Coleta de uma lista de jogos e resolução de ambiguidade
- [x] v0.3 — Armazenamento em PostgreSQL
- [x] v0.4 — Exportação para Excel
- [ ] v0.5 — API REST com FastAPI
- [ ] v0.6 — Interface web
- [ ] v0.7 — Docker (empacotamento completo da aplicação)
- [ ] v0.8 — Testes automatizados
- [ ] v0.9 — CI/CD com GitHub Actions
- [ ] v1.0 — Documentação final