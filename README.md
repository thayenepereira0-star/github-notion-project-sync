# GitHub Notion Project Sync

Automação reutilizável para sincronizar atividade de repositórios GitHub com uma base central de projetos no Notion.

O projeto nasceu de uma necessidade real: manter vários projetos do GitHub organizados no Notion sem atualizar manualmente metadados, última atividade, branch e links técnicos.

## Arquitetura

```text
VS Code
  ↓
commit / push
  ↓
GitHub repository
  ↓
caller workflow
  ↓
GitHub Notion Project Sync
  ↓
localiza projeto pelo repositório
  ↓
Notion — Projetos GitHub
```

A automação não aponta para uma página fixa. Ela usa o URL do repositório como chave e procura o projeto correspondente na base do Notion.

## O que a v1 faz

- identifica automaticamente o repositório que disparou o evento;
- consulta uma base central `Projetos GitHub` no Notion;
- encontra o projeto por `Repositório GitHub`;
- exige `Automação ativa = true` para evitar páginas-modelo;
- atualiza:
  - repositório;
  - branch principal;
  - link de Issues;
  - link de Pull Requests;
  - última atualização;
  - última atividade;
  - branch da última atividade;
- detecta referências como `#12` em commits para integrações futuras;
- falha com segurança se nenhum projeto ou mais de um projeto ativo corresponder ao mesmo repositório.

## Roadmap

### v1
- [x] roteamento por repositório
- [x] suporte a múltiplos projetos
- [x] sincronização de push
- [x] última atividade e branch
- [x] parser de referências `#issue`
- [x] proteção contra projeto duplicado

### v1.1
- [ ] Issue → tarefa no Notion
- [ ] fechamento/reabertura → status da tarefa
- [ ] identificadores idempotentes de Issue

### v1.2
- [ ] PR → tarefa
- [ ] branch e PR vinculados à tarefa
- [ ] commit `#12` → atividade da tarefa

### v1.3
- [ ] progresso automático da versão
- [ ] etapa semi-automática
- [ ] tags/Releases → versões

### v2
- [ ] testes de integração
- [ ] retries
- [ ] logs estruturados
- [ ] proteção contra concorrência
- [ ] modo dry-run

## Estrutura

```text
github-notion-project-sync/
├── action.yml
├── src/
│   ├── config.py
│   ├── events.py
│   ├── github_client.py
│   ├── notion_client.py
│   ├── sync_service.py
│   └── main.py
├── tests/
│   ├── test_events.py
│   └── test_sync_service.py
├── examples/
│   └── caller-workflow.yml
├── requirements.txt
├── .env.example
└── README.md
```

## Como usar

### 1. Prepare sua base do Notion

A base de projetos precisa ter, no mínimo:

- `Repositório GitHub` — URL
- `Automação ativa` — checkbox
- `Branches relevantes` — texto
- `Issues GitHub` — URL
- `Pull requests GitHub` — URL
- `Última atualização GitHub` — data
- `Última atividade` — texto
- `Branch da última atividade` — texto

### 2. Crie o secret

No repositório que será sincronizado, crie:

```text
NOTION_TOKEN
```

Nunca coloque o token diretamente no código ou no workflow.

### 3. Adicione o workflow chamador

Use `examples/caller-workflow.yml` como referência.

Depois que este projeto estiver publicado no GitHub, troque:

```yaml
uses: SEU_USUARIO/github-notion-project-sync@main
```

pelo caminho real do repositório.

## Desenvolvimento local

```bash
python -m venv .venv
```

Ative o ambiente virtual e instale:

```bash
pip install -r requirements.txt
```

Execute os testes:

```bash
python -m unittest discover -s tests -v
```

## Tecnologias

- Python
- REST APIs
- GitHub Actions
- GitHub API
- Notion API
- `requests`
- `unittest`

## Origem do projeto

A primeira implementação foi criada dentro do projeto `Data AI Job Market Intelligence`. Depois que a solução passou a atender vários repositórios, a integração foi extraída para um projeto independente e reutilizável.

Essa separação mantém:

- o projeto de dados responsável por dados, notebooks e análises;
- a automação responsável pela integração GitHub ↔ Notion;
- o Notion como camada de gestão;
- o GitHub como fonte da atividade técnica.
