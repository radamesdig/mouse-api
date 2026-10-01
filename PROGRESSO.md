# Progresso

## ▶ Hoje: a única coisa

**Passo 0.3: esqueleto rodando** (profundidade **S** — é ecossistema, aprende-se usando).
`git init` → `uv init` → instalar FastAPI com o `uv` → um `GET /health` que responde → `.gitignore` → **primeiro commit escrito por você**. Terminou quando `curl localhost:8000/health` responder e o `git log` mostrar o commit.
Abertura: nenhuma revisão vencida (a do 0.0 é em 09-30). Direto para o terminal.

## Nível de cobrança atual

**1 de 5**: dicas mais diretas, foco em entender os conceitos. Exceção: o **princípio 3** (um foco por sessão) já é cobrado com rigor desde o início.

---

## Trilha: desafio do Rato

```
[▶ Fase 0] → [Fase 1] → [Fase 2] → [Fase 3] → [Fase 4] → [Fase 5] → [Defesa]
 Ambiente    CRUD       Camadas    Testes     Mensageria  Docker     REFLEXAO.md
 e Git       feio       e SOLID               (RabbitMQ)  e README   + oral
```

Profundidade: **E** = Essencial · **S** = Só o suficiente · **X** = Estacionar

### ▶ Fase 0: ambiente e Git (atual)

| # | Passo | Prof. | Por que agora | Feito |
|---|---|:-:|---|:-:|
| 0.0 | Entender o problema central: por que a notificação não pode ser síncrona | E | É o coração do desafio e guia todas as decisões | ☑ `notas/0.0-por-que-fila.md` |
| 0.1 | Terminal: navegar em pastas e rodar comandos | S | Tudo o que vem depois roda no terminal | ☑ `notas/0.1-terminal.md` |
| 0.2 | Versões de Python: o que é o pyenv, se está instalado, quais versões existem | S *(era E — rebaixado em 25/09: é ecossistema)* | O desafio exige Python 3.12+ | ☑ `notas/0.2-pyenv.md` |
| 0.3 | **Esqueleto rodando:** `git init` + `uv init` + FastAPI + `GET /health` + `.gitignore` + 1º commit | S | É o fim da Fase 0. Os antigos passos 0.3–0.7 viraram um só: `uv`, Git e `.gitignore` se aprendem fazendo o esqueleto | ☐ |

> 🔪 **Reorganizado em 2026-09-25 pelo princípio de Karpathy (núcleo × ecossistema).** A Fase 0 tinha 8 passos antes do primeiro endpoint — isso é preparar-se para construir, não construir. GitHub remoto, branch e PR entram na **Fase 1**, na primeira funcionalidade (o desafio exige branch por feature: aprende-se ali).

### Fase 1: CRUD numa camada só ("feio, mas funciona")

*(começa com: repositório no GitHub + a 1ª branch de feature → PR → merge, na primeira rota do CRUD)*


HTTP e REST (métodos, status, JSON) **S** · FastAPI básico e Swagger **E** · Pydantic v2 **E** · Docker só para subir o Postgres **S** · SQL básico e constraint `UNIQUE` **S** · SQLAlchemy 2.x **E** · Alembic **S** · paginação e filtros **E** · algoritmo do CPF e regra da idade **E** · semântica dos status 400/404/409/422 **E** · `pydantic-settings` e `.env` **E**

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

- Definição precisa de acoplamento: não só "A depende de B", mas *o quanto* A sabe sobre B e o que acontece com A quando B muda ou cai.

## Estacionamento

_Temas que apareceram fora do foco. Não se perdem, mas também não entram agora._

- Bônus do desafio: JWT, Prometheus, rate limiting (**X**: só depois que o projeto estiver completo)
- **"E se o próprio quadro de recados sumir?"** (a "regra de ouro" do Rato, seção 3.3). Sua primeira hipótese: *caching*. Volta na Fase 4, onde vamos testar essa hipótese.
- Homebrew por dentro: como ele funciona e para que serve exatamente (**X**: por enquanto basta saber que é um gerenciador de pacotes que instala em `/opt/homebrew`)
- Onde fica configurado o alias `python` → `python3` (arquivo de configuração do shell) (**S**: volta se aparecer no 0.3)

## Diário

| Sessão | O que consigo fazer agora que não conseguia antes |
|---|---|
| 2026-09-23 · 0.0 · por que fila | Compreendo melhor a ideia de acoplamento |
| 2026-09-24 · 0.1 · terminal | Navego até qualquer pasta pelo terminal, sei sempre onde estou e entendi por que o terminal começa na home |
| 2026-09-24 · 0.2 · versões de python | Sei que o pyenv foi instalado pelo Homebrew e navego até a pasta dele para explorar como o gerenciador de versões funciona |
