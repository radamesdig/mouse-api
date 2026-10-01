# Desafio Técnico — API de Cadastro de Pessoas com Mensageria

**Nível:** Júnior avançado / Pleno
**Estimativa:** 25 a 40 horas de trabalho
**Linguagem:** Python 3.12+
**Modalidade:** Individual, sem uso de IA generativa

---

## 1. O contexto

Você foi contratado pela **Cadastra**, uma empresa que centraliza cadastro de pessoas físicas para outras empresas do grupo. Hoje o cadastro é feito numa planilha compartilhada. Sua missão é construir o serviço que vai substituir essa planilha.

O detalhe importante: sempre que uma pessoa é cadastrada ou atualizada, **outros sistemas do grupo precisam ser notificados** — o sistema de e-mail marketing, o de compliance e o de BI. Você não vai construir esses sistemas. Você vai construir a API e publicar os eventos numa fila para que eles consumam depois.

Esse é o ponto central do desafio: entender por que a notificação **não pode** acontecer de forma síncrona dentro do request HTTP.

---

## 2. O que você vai entregar

Um repositório Git com:

- Uma API REST funcional
- Um worker consumidor de mensagens
- Suíte de testes automatizados
- `docker-compose.yml` que sobe tudo com um comando
- `README.md` que permita a qualquer pessoa rodar o projeto sem te perguntar nada

---

## 3. Requisitos funcionais

### 3.1 Modelo de dados

Uma pessoa tem:

| Campo | Tipo | Regras |
|---|---|---|
| `id` | UUID | Gerado pelo sistema, imutável |
| `nome_completo` | string | Obrigatório, 3 a 150 caracteres |
| `cpf` | string | Obrigatório, único, **validar dígito verificador** |
| `email` | string | Obrigatório, único, formato válido |
| `data_nascimento` | date | Obrigatório, não pode ser futura, pessoa deve ter ≥ 18 anos |
| `telefone` | string | Opcional, formato E.164 (`+5521999998888`) |
| `ativo` | boolean | Default `true` |
| `criado_em` | datetime | UTC, gerado pelo sistema |
| `atualizado_em` | datetime | UTC, atualizado a cada alteração |

> **Atenção:** validar CPF é validar o **dígito verificador**, não só contar 11 caracteres. Implemente o algoritmo. Não use biblioteca pronta — é justamente o tipo de lógica de domínio que o desafio quer ver você escrevendo e testando.

### 3.2 Endpoints

| Método | Rota | Descrição | Status de sucesso |
|---|---|---|---|
| `POST` | `/api/v1/pessoas` | Cria uma pessoa | `201 Created` |
| `GET` | `/api/v1/pessoas` | Lista pessoas (paginado + filtros) | `200 OK` |
| `GET` | `/api/v1/pessoas/{id}` | Busca por ID | `200 OK` |
| `PUT` | `/api/v1/pessoas/{id}` | Atualiza dados | `200 OK` |
| `DELETE` | `/api/v1/pessoas/{id}` | Remove (soft delete) | `204 No Content` |
| `POST` | `/api/v1/pessoas/{id}/notificacoes` | **Dispara notificação assíncrona** | `202 Accepted` |
| `GET` | `/health` | Healthcheck (API + banco + broker) | `200 OK` |

**Regras da listagem:**
- Paginação obrigatória via `?page=1&size=20`, com `size` máximo de 100
- Filtros: `?nome=`, `?cpf=`, `?ativo=`
- Resposta deve conter os metadados: `total`, `page`, `size`, `items`

**Regras de status HTTP** — respeite a semântica:
- `400` — JSON malformado ou parâmetro inválido
- `404` — recurso não encontrado
- `409` — conflito (CPF ou e-mail já cadastrado)
- `422` — payload bem formado mas com violação de regra de negócio (CPF inválido, menor de idade)
- `500` — só para o que você realmente não previu

**Contrato de erro padronizado.** Toda resposta de erro deve seguir o mesmo formato em toda a API:

```json
{
  "erro": "VALIDACAO",
  "mensagem": "Dados inválidos",
  "detalhes": [
    { "campo": "cpf", "problema": "dígito verificador inválido" }
  ],
  "trace_id": "9f2b1c40-3d5e-4a11-b8c7-0e2f5a1d9c33"
}
```

### 3.3 O endpoint assíncrono

`POST /api/v1/pessoas/{id}/notificacoes`

Esse endpoint **não faz o trabalho** — ele enfileira o trabalho.

**Comportamento esperado:**
1. Valida que a pessoa existe (`404` se não)
2. Monta um evento e publica na fila do RabbitMQ
3. Retorna `202 Accepted` **imediatamente**, sem esperar o processamento
4. A resposta inclui um identificador para acompanhamento

```json
{
  "notificacao_id": "a3f8...",
  "status": "ENFILEIRADA",
  "pessoa_id": "b71c..."
}
```

> **A regra de ouro:** se o RabbitMQ estiver fora do ar, o endpoint deve falhar de forma explícita e controlada (`503 Service Unavailable`) — nunca retornar `202` mentindo que enfileirou. Isso é um erro clássico e o desafio vai cobrar.

**Eventos automáticos.** Além do endpoint manual, a criação (`POST /pessoas`) e a atualização (`PUT /pessoas/{id}`) também devem publicar eventos — `pessoa.criada` e `pessoa.atualizada`. Aqui aparece um problema real: se o banco commita mas a publicação falha, você perdeu o evento. Documente no README como você lidou com isso. (Investigue o termo **Transactional Outbox** — implementar é bônus, mas você precisa saber que o problema existe.)

---

## 4. Requisitos técnicos obrigatórios

### 4.1 Stack

| Camada | Tecnologia |
|---|---|
| Runtime | Python 3.12+ |
| Framework web | FastAPI (recomendado) ou Flask |
| Banco | PostgreSQL 16 |
| ORM | SQLAlchemy 2.x |
| Migrations | Alembic |
| Broker | RabbitMQ 3.13 |
| Cliente AMQP | `pika` ou `aio-pika` |
| Validação | Pydantic v2 |
| Testes | `pytest` + `pytest-cov` + `httpx` |
| Container | Docker + Docker Compose |
| Gerência de deps | `uv`, Poetry ou `pip-tools` — **não** um `requirements.txt` escrito à mão |

**Proibido:** SQLite, dicionário em memória como "banco", ou salvar em arquivo JSON.

### 4.2 Configuração

- **Nenhum** valor sensível ou de ambiente hardcoded no código
- Toda config via variáveis de ambiente, carregadas por `pydantic-settings`
- `.env.example` versionado com todas as variáveis; `.env` real no `.gitignore`
- A aplicação deve **falhar no boot** se uma variável obrigatória estiver faltando — não descobrir isso no primeiro request

### 4.3 Qualidade de código

Configure e deixe passando:

- `ruff` (lint + format)
- `mypy` em modo estrito nas camadas de domínio e aplicação
- `pre-commit` rodando os dois acima

Type hints em **todas** as funções públicas. Sem exceção.

### 4.4 Logging

- Log estruturado em JSON (`structlog` ou `logging` configurado)
- `trace_id` propagado do request até o consumer da fila — quando algo quebra, você precisa conseguir seguir o rastro
- **Nunca** logar CPF completo, e-mail ou telefone. Mascare (`***.***.789-00`). Isso não é preciosismo: é LGPD.

---

## 5. Arquitetura e boas práticas

### 5.1 Separação em camadas

O projeto deve ter fronteiras claras. Sugestão:

```
src/
├── domain/              # Entidades e regras de negócio puras
│   ├── entities/        # Pessoa — sem SQLAlchemy, sem FastAPI
│   ├── value_objects/   # CPF, Email, Telefone
│   ├── exceptions/      # CpfInvalidoError, PessoaNaoEncontradaError
│   └── repositories/    # INTERFACES (ABC), não implementações
├── application/         # Casos de uso
│   ├── use_cases/       # CriarPessoaUseCase, ListarPessoasUseCase...
│   └── dtos/
├── infrastructure/      # O mundo externo
│   ├── database/        # SQLAlchemy, models, implementação dos repos
│   ├── messaging/       # RabbitMQ publisher e consumer
│   └── config/
├── presentation/        # HTTP
│   ├── api/v1/routes/
│   ├── schemas/         # Pydantic request/response
│   └── middlewares/
└── main.py
tests/
├── unit/
├── integration/
└── e2e/
```

**O teste que prova que você acertou:** o código em `domain/` não pode ter *nenhum* `import` de FastAPI, SQLAlchemy ou pika. Se tiver, sua regra de negócio está acoplada à infraestrutura. Rode `grep -r "sqlalchemy\|fastapi\|pika" src/domain/` — tem que voltar vazio.

### 5.2 SOLID — aplicado, não decorado

Você vai precisar **demonstrar cada princípio** no README, apontando arquivo e linha:

- **SRP** — Cada caso de uso faz uma coisa. Se sua classe `PessoaService` tem 400 linhas e 12 métodos, você errou.
- **OCP** — Adicionar um novo tipo de notificação não pode exigir editar o publisher existente.
- **LSP** — Seu repositório fake usado nos testes tem que ser substituível pelo real sem quebrar nada.
- **ISP** — Prefira `PessoaLeituraRepository` e `PessoaEscritaRepository` a uma interface gorda com 15 métodos.
- **DIP** — O caso de uso depende da **interface** do repositório, nunca da implementação SQLAlchemy. A injeção acontece na borda da aplicação.

### 5.3 Clean Code

- Nomes em português **ou** inglês — escolha um e seja consistente no projeto inteiro
- Funções curtas. Se passou de ~20 linhas, provavelmente faz mais de uma coisa
- Sem números mágicos — constantes nomeadas
- Sem comentário explicando *o que* o código faz; se precisa, renomeie. Comentário serve para explicar *por quê*
- Exceções de domínio próprias, nunca `raise Exception("erro")`
- Early return em vez de `if` aninhado em três níveis

---

## 6. Mensageria

### 6.1 Topologia

Configure no RabbitMQ:

- **Exchange:** `pessoas.events` (tipo `topic`)
- **Routing keys:** `pessoa.criada`, `pessoa.atualizada`, `pessoa.notificacao`
- **Filas:** uma por consumidor lógico, com binding apropriado
- **Dead Letter Queue:** `pessoas.events.dlq` — mensagem que falha 3 vezes vai pra cá

### 6.2 Contrato da mensagem

```json
{
  "evento_id": "uuid",
  "tipo": "pessoa.criada",
  "versao": "1.0",
  "ocorrido_em": "2026-08-21T14:32:10Z",
  "trace_id": "uuid",
  "dados": {
    "pessoa_id": "uuid",
    "nome_completo": "Maria Silva",
    "email": "maria@exemplo.com"
  }
}
```

### 6.3 O consumer

Um processo separado (não uma thread dentro da API) que:

- Consome as mensagens e simula o processamento (um `sleep` + log estruturado já basta)
- Faz `ack` só **depois** do sucesso, `nack` em caso de falha
- Implementa **retry com backoff exponencial** — 3 tentativas, depois DLQ
- É **idempotente**: receber a mesma mensagem duas vezes não pode causar efeito duplicado. Brokers entregam duplicado, é normal. Trate.
- Encerra graciosamente com `SIGTERM` — termina a mensagem em andamento antes de morrer

> Reflita e escreva no README: qual a diferença entre `async def` no FastAPI e processamento assíncrono via fila? São coisas diferentes resolvendo problemas diferentes. Se você não souber explicar isso, ainda não entendeu o desafio.

---

## 7. Testes

### 7.1 Cobertura mínima

- **80% global**, medido com `pytest-cov`
- **95% na camada `domain/`** — é a sua regra de negócio, tem que estar blindada
- O build deve **falhar** se a cobertura cair abaixo do mínimo (`--cov-fail-under=80`)

### 7.2 O que testar

**Unitários** (rápidos, sem I/O, sem Docker):
- Validação de CPF — casos válidos, inválidos, com máscara, todos os dígitos iguais (`111.111.111-11` é inválido)
- Regra de idade mínima, incluindo o caso de aniversário hoje
- Cada caso de uso, com repositório fake injetado
- Serialização/desserialização do evento

**Integração** (com Docker subindo Postgres e RabbitMQ):
- Repositório contra banco real — inclusive violação de constraint única
- Publicação real de mensagem no RabbitMQ
- Consumer processando mensagem de verdade
- Fluxo de DLQ após 3 falhas

**E2E:**
- `POST /pessoas` → verifica resposta HTTP → verifica registro no banco → verifica mensagem na fila
- Caminhos de erro: CPF duplicado, menor de idade, ID inexistente

### 7.3 Como os testes devem rodar

Isso é requisito de entrega, não detalhe:

```bash
make test           # tudo
make test-unit      # só unitários, sem Docker, < 5 segundos
make test-integration
make coverage       # gera relatório HTML em htmlcov/
```

**Exigências:**
- Testes de integração usam **Testcontainers** ou um `docker-compose.test.yml` dedicado — nunca o banco de desenvolvimento
- Banco limpo entre testes (transação com rollback ou truncate em fixture)
- Nenhum teste depende da ordem de execução — `pytest-randomly` deve passar
- Use `pytest.mark.parametrize` em vez de copiar e colar o mesmo teste com valores diferentes
- Fixtures em `conftest.py`, sem duplicação

---

## 8. Docker

### 8.1 O comando único

Isto precisa funcionar numa máquina limpa, recém-clonada:

```bash
docker compose up -d
```

E subir: API, PostgreSQL, RabbitMQ (com painel de administração), consumer worker.

### 8.2 Exigências

- **Multi-stage build** — imagem final sem compilador, sem dependências de dev
- Container roda com **usuário não-root**
- `healthcheck` em todos os serviços
- `depends_on` com `condition: service_healthy` — a API não pode subir antes do banco estar pronto
- Volume nomeado para persistir os dados do Postgres
- Migrations aplicadas automaticamente no start
- `.dockerignore` decente
- **Meta:** imagem final abaixo de 200 MB

---

## 9. README

O README é entregável avaliado. O critério é simples: **uma pessoa que nunca viu o projeto consegue rodá-lo em menos de 5 minutos, sem te perguntar nada?**

Deve conter:

1. **Descrição** — o que o projeto faz, em dois parágrafos
2. **Stack** — tecnologias e por que cada uma foi escolhida
3. **Arquitetura** — diagrama (Mermaid ou ASCII) mostrando API → RabbitMQ → Consumer, e a estrutura de pastas explicada
4. **Pré-requisitos** — versões exatas
5. **Como rodar** — passo a passo copiável, do `git clone` até a API respondendo
6. **Variáveis de ambiente** — tabela com nome, descrição, valor padrão, obrigatória sim/não
7. **Como rodar os testes** — os comandos e o que cada suíte cobre
8. **Documentação da API** — link do Swagger + ao menos um exemplo de `curl` por endpoint, com request e response reais
9. **Como observar a mensageria** — como acessar o painel do RabbitMQ (`localhost:15672`), onde ver a fila crescendo, como forçar uma mensagem pra DLQ
10. **Decisões de arquitetura** — as escolhas que você fez e os trade-offs que aceitou
11. **Onde estão os princípios SOLID** — arquivo e linha para cada um
12. **O que ficou de fora** — seja honesto sobre limitações conhecidas

---

## 10. Regras

### 10.1 Sem IA

**Proibido:** ChatGPT, Claude, Copilot, Cursor, Gemini ou qualquer assistente para gerar código, testes, configuração ou o README.

**Permitido e incentivado:** documentação oficial, Stack Overflow, livros, tutoriais, blog posts, o código-fonte das bibliotecas que você usa.

O motivo não é purismo. É que quem cola o código do modelo aprende a *reconhecer* a solução, não a *construir* — e trava na primeira vez que precisa depurar algo que o modelo não previu. Aqui o objetivo é você travar, procurar, entender e destravar. É esse ciclo que constrói o programador.

**Verificação:** ao final, você vai defender o projeto oralmente. Perguntas do tipo *"por que você escolheu topic exchange em vez de direct?"*, *"o que acontece se o consumer cair no meio do processamento?"*, *"por que essa interface está no domain e a implementação na infrastructure?"*. Código que você não sabe explicar é código que não conta.

### 10.2 Git

- Commits pequenos e atômicos, em **Conventional Commits** (`feat:`, `fix:`, `test:`, `docs:`, `refactor:`)
- Mínimo 20 commits — o histórico precisa contar a história do desenvolvimento
- Uma branch por funcionalidade, merge na `main` via PR (mesmo sendo você sozinho)
- Nada de um único commit gigante chamado "projeto pronto"

---

## 11. Como avaliar (100 pontos)

| Área | Pontos | O que se olha |
|---|---:|---|
| Funcionalidade | 20 | Todos os endpoints funcionam conforme especificado |
| Arquitetura e SOLID | 20 | Camadas independentes, dependências apontando pra dentro |
| Testes | 20 | Cobertura atingida, testes significativos, rodam fácil |
| Mensageria | 15 | Publicação, consumo, retry, DLQ, idempotência |
| Docker | 10 | Sobe com um comando numa máquina limpa |
| README | 10 | Alguém consegue rodar sem ajuda |
| Clean Code | 5 | Nomes, tamanho de função, ausência de duplicação |

**Bônus (+5 cada, máximo +15):** Transactional Outbox implementado · CI no GitHub Actions rodando lint, mypy e testes · métricas Prometheus · rate limiting · autenticação JWT nos endpoints de escrita.

**Zera a entrega:** uso de IA detectado · testes que não rodam · `docker compose up` que não sobe · segredos commitados no repositório.

---

## 12. Ordem sugerida de execução

Não tente fazer tudo de uma vez. Ataque em fases, com o projeto rodando ao final de cada uma:

| Fase | Foco | Tempo |
|---|---|---|
| **1** | CRUD funcionando: FastAPI + Postgres + Alembic, tudo numa camada só. Feio, mas funciona. | 6–8h |
| **2** | Refatorar para as camadas. Extrair domínio, criar interfaces, inverter dependências. **Aqui você aprende SOLID de verdade** — sentindo a dor de código acoplado antes de desacoplar. | 6–10h |
| **3** | Testes unitários e de integração até bater a cobertura. | 6–8h |
| **4** | RabbitMQ: publisher, consumer, retry, DLQ, idempotência. | 6–10h |
| **5** | Docker, README, polimento, CI. | 4–6h |

A Fase 2 é a mais importante do desafio. Resista à tentação de já começar com a arquitetura pronta — escrever o código acoplado primeiro e sentir por que ele incomoda é o que faz a lição colar.

---

## 13. Perguntas para responder ao final

Escreva as respostas num arquivo `REFLEXAO.md`. Se você não conseguir responder com suas palavras, volte e estude:

1. Qual a diferença entre concorrência e paralelismo? Onde cada uma aparece nesse projeto?
2. Por que `async def` no FastAPI não resolve o problema que a fila resolve?
3. O que acontece se o consumer receber a mesma mensagem duas vezes? Como seu código lida?
4. Por que a interface do repositório fica em `domain/` e a implementação em `infrastructure/`?
5. Como você garantiria que um evento não se perde se o banco commitar e o RabbitMQ cair no instante seguinte?
6. Qual foi a parte mais difícil? Como você descobriu a solução?

---

**Boa sorte. Trave, procure, entenda, destrave. É assim que funciona.**
