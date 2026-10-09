# Progresso

## ▶ Hoje: a única coisa

**Abertura:** revisões vencidas, sem consulta: **3ª do 0.0 · por que fila** (vence em 10-08; cobrar os **três nomes** de primeira) e, se já for 10-11, **2ª do 1.1 · modelo Pydantic** (cobrar o "valida **antes** da função" de primeira). O "de cabeça" da sessão anterior: explicar o que o `**` faz em `RetornarPessoa(**pessoa_entrada.model_dump(), ...)`.
**Depois: passo 1.2.** Nova branch a partir da `main` atualizada → `GET /api/v1/pessoas` (lista) e `GET /api/v1/pessoas/{id}` (busca na `lista_de_pessoas_saida`) → `404` quando o `id` não existe. É aqui que entra o mínimo de **HTTP** que ficou estacionado (servidor × cliente, pedido × resposta, verbo, status).

## Nível de cobrança atual

**1 de 5**: dicas mais diretas, foco em entender os conceitos. Exceção: o **princípio 3** (um foco por sessão) já é cobrado com rigor desde o início.

---

## Trilha: desafio do Rato

```
[Fase 0 ✓] → [▶ Fase 1] → [Fase 2] → [Fase 3] → [Fase 4] → [Fase 5] → [Defesa]
 Ambiente    CRUD       Camadas    Testes     Mensageria  Docker     REFLEXAO.md
 e Git       feio       e SOLID               (RabbitMQ)  e README   + oral
```

Profundidade: **E** = Essencial · **S** = Só o suficiente · **X** = Estacionar

### Fase 0: ambiente e Git ✓ (terminada em 2026-10-01)

| # | Passo | Prof. | Por que agora | Feito |
|---|---|:-:|---|:-:|
| 0.0 | Entender o problema central: por que a notificação não pode ser síncrona | E | É o coração do desafio e guia todas as decisões | ☑ `notas/0.0-por-que-fila.md` |
| 0.1 | Terminal: navegar em pastas e rodar comandos | S | Tudo o que vem depois roda no terminal | ☑ `notas/0.1-terminal.md` |
| 0.2 | Versões de Python: o que é o pyenv, se está instalado, quais versões existem | S *(era E — rebaixado em 25/09: é ecossistema)* | O desafio exige Python 3.12+ | ☑ `notas/0.2-pyenv.md` |
| 0.3 | **Esqueleto rodando:** `git init` + `uv init` + FastAPI + `GET /health` + `.gitignore` + 1º commit | S | É o fim da Fase 0. Os antigos passos 0.3–0.7 viraram um só: `uv`, Git e `.gitignore` se aprendem fazendo o esqueleto | ☑ commit `ae7723d` |

> 🔪 **Reorganizado em 2026-09-25 pelo princípio de Karpathy (núcleo × ecossistema).** A Fase 0 tinha 8 passos antes do primeiro endpoint — isso é preparar-se para construir, não construir. GitHub remoto, branch e PR entram na **Fase 1**, na primeira funcionalidade (o desafio exige branch por feature: aprende-se ali).

### ▶ Fase 1: CRUD numa camada só ("feio, mas funciona") (atual)

*Detalhada em 2026-10-01. Começa **sem banco** (dados numa lista em memória) para que você sinta a falta da persistência antes de trazê-la. Cada passo = uma branch de feature → PR → merge.*

| # | Passo | Prof. | Por que agora | Feito |
|---|---|:-:|---|:-:|
| 1.1 | `POST /api/v1/pessoas` guardando em memória · Pydantic (campos e tipos) · `201` · **GitHub remoto, branch e PR** | E (Pydantic) · S (Git/HTTP) | É a primeira funcionalidade do CRUD; o desafio exige branch por feature | ☑ PR #1 com merge na `main` (`66d31a9`) |
| 1.2 | `GET` lista e `GET` por id, em memória · `404` | E | Ler o que foi criado; primeiro status de erro | ☐ |
| 1.3 | `PUT` e `DELETE` (soft delete) · `204` | E | Fecha o CRUD | ☐ |
| 1.4 | Algoritmo do CPF e regra da idade ≥ 18 · nome 3–150, formato do e-mail e telefone E.164 *(vieram do 1.1)* · `422` | E | Lógica de domínio que o desafio quer ver escrita à mão | ☐ |
| 1.5 | Postgres subindo no Docker + SQL básico e `UNIQUE` | S | Reiniciar o servidor apaga a lista: chegou a hora do banco | ☐ |
| 1.6 | `pydantic-settings` e `.env` (a URL do banco) | E | Primeiro segredo do projeto — liga com o `.gitignore` do 0.3 | ☐ |
| 1.7 | SQLAlchemy 2.x: trocar a lista em memória pelo banco | E | Persistência de verdade | ☐ |
| 1.8 | Alembic: a primeira migração | S | O desafio exige migrações, não `create_all` | ☐ |
| 1.9 | `409` para CPF/e-mail duplicado | E | Semântica de status: conflito × regra de negócio | ☐ |
| 1.10 | Paginação (`page`, `size` ≤ 100) e filtros (`nome`, `cpf`, `ativo`) | E | Fecha os requisitos da listagem | ☐ |

### Fase 2: refatorar para as camadas (a mais importante)

Por que código acoplado dói **E** · classes abstratas (`abc`) e interfaces **E** · injeção de dependência **E** · SOLID na prática **E** · exceções de domínio **E** · contrato de erro padronizado **E**

### Fase 3: testes e qualidade

`pytest`, fixtures e `parametrize` **E** · repositório fake **E** · cobertura (`pytest-cov`) **E** · Testcontainers **S** · Makefile **S** · `ruff`, `mypy` e `pre-commit` **S**

### Fase 4: mensageria

Concorrência × paralelismo e `async def` × fila **E** · RabbitMQ: exchange, queue, routing key, ack **E** · `pika`/`aio-pika` **S** · retry com backoff e DLQ **E** · idempotência **E** · SIGTERM **S** · log estruturado, `trace_id` e mascaramento (LGPD) **E** · Transactional Outbox, só o conceito **S**

### Fase 5: entrega

Docker multi-stage, usuário não-root, healthcheck **S** · README avaliado **E** · CI no GitHub Actions (bônus) **S**

### Defesa

`REFLEXAO.md` (6 perguntas) **E** · simulação da defesa oral **E**

---

## Domina

_Só entra aqui o que você já reproduziu ou explicou sem consulta._

- Os 3 problemas do fluxo síncrono — lentidão, acoplamento e falha parcial — e por que eles justificam a fila. Explicado sem consulta em 2026-09-24.
- Navegar no terminal: `pwd`, `cd`, `ls -a`, os atalhos `~`, `.` e `..`, a árvore a partir de `/` e o Tab.
- Investigar uma ferramenta de terminal por conta própria: `--version`, `which`, `--help` e subcomando × opção (`pyenv versions` × `--version`). Feito sozinho, errando e corrigindo pela ajuda da própria ferramenta, em 2026-09-24.

## Reconheço, mas ainda não faço sozinho

- *(ecossistema, S — não precisa ir para "Domina")* Como o pyenv escolhe a versão: shim → `pyenv` → arquivo `~/.pyenv/version` → `~/.pyenv/versions/<versão>/bin/python3`. Chegou à conclusão com perguntas guiadas. Na nota, ainda confundiu o arquivo `version` com a pasta `versions`.
- *(ecossistema, S)* Por que não usar o Python `system` do macOS.

- `GET /health` devolve `200 OK` sem você escrever o número: o FastAPI responde 200 quando a função termina normalmente. O `/health` é para um monitor perguntar "está vivo?". Viu no `curl -i` em 2026-10-01.
- *(ecossistema, S)* Regra do `.gitignore`, formulada por você: **o que pode ser recriado a partir de outro arquivo não vai para o Git** (`.venv`, `__pycache__`), e **segredo nunca vai** (zera a entrega — seção 11). Na 1ª versão, ignorou `pyproject.toml`, `uv.lock` e `.*` por engano; corrigiu com perguntas.
- *(ecossistema, S)* `uv.lock` × `pyproject.toml`: o `>=` aceita versões novas; o lock anota as versões exatas. Na pergunta de defesa ainda disse que "o `uv.lock` não pode ser recriado" — o ponto é que recriá-lo pode trazer **outras** versões.

- Modelo Pydantic como "formulário" na porta da API: um modelo de **entrada** (o que o cliente manda) e um de **saída** (o que ele recebe, com o que o sistema gera). O FastAPI valida **antes** da função rodar e devolve `422` listando **todos** os campos com problema. Viu e previu no `curl` em 2026-10-04.
- Por que `id` é UUID e não sequencial: **enumeração** (dados pessoais, LGPD). Respondeu com uma pista.
- Status de sucesso fica no **decorador** (`status_code=201`), porque faz parte do contrato da rota; os **parâmetros da função** são o que chega na requisição. *(Em 2026-10-06 explicou sozinho por que `pessoa_saida` não pode ser parâmetro: o cliente teria que mandar `id`, `ativo` e datas.)*
- `pessoa_entrada: CriarPessoa` é **anotação de tipo**: quem cria o objeto é o FastAPI (lê o JSON → valida → instancia → passa para a função). Disse sozinho que, sem `cpf`, "o objeto nem chega a ser criado".
- **Classe × objeto**: `RetornarPessoa` é o molde, `pessoa_entrada` é o formulário preenchido. A 1ª tentativa foi `RetornarPessoa.model_dump()` (na classe); corrigiu com perguntas. Vocabulário: "instanciar a classe" / "instância da classe".
- **`**` desfaz a mala**: na **chamada**, espalha um `dict` em `campo=valor`; na **definição** (`def f(**kwargs)`), junta. Montou sozinho `RetornarPessoa(**pessoa_entrada.model_dump(), id=..., ...)` e explicou o ganho: campo novo só muda no modelo. Travou bastante antes (vídeos sobre `**kwargs` confundiram as direções).
- **Bug silencioso**: campo opcional esquecido vira `null` sem erro (o `telefone`). O obrigatório grita `Field required`, o opcional não. Erro de validação **dentro** da função vira `500`, não `422`.
- Gerar a hora **uma vez** numa variável (`agora`) para `criado_em` e `atualizado_em`, e com `timezone.utc`.
- Variável criada dentro da função recomeça a cada chamada; a lista em memória fica **fora**. Hipótese inicial era "dentro" — corrigiu pelo experimento. Reiniciar o servidor apaga a lista (a dor que traz o banco no 1.5).
- `default_factory`: por que não `= datetime.now(...)` direto (a classe é definida uma vez só, quando o servidor sobe). Explicou com as próprias palavras.
- *(Python)* Iterar um `dict` dá só as **chaves** (o `+=` com `model_dump()` deu 5). Chamar uma classe com valores **pelo nome** (`campo=valor`), `=` × `==`, `True` maiúsculo — ainda trava aqui.
- *(ecossistema, S)* Ler traceback: achar a única linha do **seu** arquivo e a última linha (o erro). `NameError` (variável não existe) × `AttributeError` (o objeto existe, mas não tem esse atributo).
- *(ecossistema, S)* Primeiro PR: `git push -u origin <branch>`, base × compare, descrição com **como testar e o que esperar**, merge pelo GitHub, `git pull` e o **commit de merge**. Recusou certo o `git push origin HEAD:main` (ia direto para a `main`, sem PR) e consertou o upstream errado.

- Definição precisa de acoplamento: não só "A depende de B", mas *o quanto* A sabe sobre B e o que acontece com A quando B muda ou cai.

## Estacionamento

_Temas que apareceram fora do foco. Não se perdem, mas também não entram agora._

- Bônus do desafio: JWT, Prometheus, rate limiting (**X**: só depois que o projeto estiver completo)
- Por que a `.venv` só funciona na sua máquina (e não no computador do Rato ou num servidor Linux) (**S**: volta na Fase 5, com Docker)
- Por que `async def` e não `def` no endpoint (**E**: já está na Fase 4 — "concorrência × paralelismo e `async def` × fila")
- **"E se o próprio quadro de recados sumir?"** (a "regra de ouro" do Rato, seção 3.3). Sua primeira hipótese: *caching*. Volta na Fase 4, onde vamos testar essa hipótese.
- Homebrew por dentro: como ele funciona e para que serve exatamente (**X**: por enquanto basta saber que é um gerenciador de pacotes que instala em `/opt/homebrew`)
- Primeira linha do commit curta (~50 caracteres), dizendo o resultado (**S**: cobrar aos poucos nos próximos commits)
- Onde fica configurado o alias `python` → `python3` (arquivo de configuração do shell) (**X**: não apareceu no 0.3)
- O que é servidor, cliente (`curl`), programa/processo e HTTP; como os dois conversam (**E**: entra no **1.2**, com `GET` e `404`. Ganchos de hoje: o `print` aparece no servidor e não no `curl`; função sem `return` → `null`)
- Diferença entre uma classe do Pydantic (herda de `BaseModel`) e uma classe comum do Python (**S**: volta na Fase 2, quando o domínio tiver classes próprias sem Pydantic)

## Diário

| Sessão | O que consigo fazer agora que não conseguia antes |
|---|---|
| 2026-09-23 · 0.0 · por que fila | Compreendo melhor a ideia de acoplamento |
| 2026-09-24 · 0.1 · terminal | Navego até qualquer pasta pelo terminal, sei sempre onde estou e entendi por que o terminal começa na home |
| 2026-09-24 · 0.2 · versões de python | Sei que o pyenv foi instalado pelo Homebrew e navego até a pasta dele para explorar como o gerenciador de versões funciona |
| 2026-09-26 · 0.3 · esqueleto rodando | Consigo criar rotas, subir um servidor com FastAPI, definir o que colocar no `.gitignore` e usar o `--help` quando não sei o que fazer |
| 2026-10-01 · 1.1 · criar pessoa em memória | Consigo declarar uma classe do Pydantic de forma consciente |
| 2026-10-06 · 1.1 · modelo de saída | Agora consigo criar um fluxo completo de entrada e saída de dados numa rota de uma API |
