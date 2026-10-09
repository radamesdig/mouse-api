# Revisões espaçadas

Acompanha as revisões de cada nota. A revisão é **sem consulta**: você explica ou reproduz o assunto de cabeça, e só depois abre a nota para conferir.

**Intervalos:** 1ª em 24h · 2ª em 7 dias · 3ª em 15 dias · 4ª, 5ª e 6ª de 30 em 30 dias.

**Só entra aqui o NÚCLEO** (ver "Núcleo × ecossistema" no `AGENTS.md`). Ferramenta se fixa usando, não revisando. *(0.1 terminal e 0.2 pyenv saíram da agenda em 2026-09-25 por isso — as notas continuam em `notas/`.)*

**Regras**
- A revisão acontece na **abertura** da sessão, em poucos minutos. Ela nunca vira o foco do dia.
- Atrasou? Faça na próxima sessão e **não recalcule** as datas seguintes — elas continuam contadas a partir do dia em que o assunto foi estudado.
- Errou feio na revisão? O item volta para "Reconheço, mas ainda não faço sozinho" no `PROGRESSO.md` e a contagem recomeça da 1ª.
- Depois da 6ª, o assunto sai desta tabela. A essa altura ele já está sendo usado no projeto todo dia.

## Agenda

| Nota | Assunto | Estudado | 1ª (24h) | 2ª (7d) | 3ª (15d) | 4ª (+30d) | 5ª (+30d) | 6ª (+30d) |
|---|---|---|---|---|---|---|---|---|
| [0.0](notas/0.0-por-que-fila.md) | Por que a notificação vai para uma fila | 2026-09-23 | ☑ 09-24 | ☑ 10-01 | ☐ 10-08 | ☐ 11-07 | ☐ 12-07 | ☐ 2027-01-06 |
| [1.1](notas/1.1-classe-pydantic.md) | Modelo Pydantic: entrada × saída e validação na porta da API | 2026-10-04 | ☑ 10-06 | ☐ 10-11 | ☐ 10-19 | ☐ 11-18 | ☐ 12-18 | ☐ 2027-01-17 |

## Histórico

| Data | Nota | Revisão | Como foi |
|---|---|---|---|
| 2026-09-24 | 0.0 | 1ª | Explicou os 3 problemas sem consulta. Foi para "Domina". |
| 2026-10-01 | 0.0 | 2ª (1 dia de atraso) | Com ajuda. De primeira, lembrou só de falha parcial (e citou deduplicação, que é da Fase 4). Com perguntas, explicou lentidão e acoplamento pelo mecanismo, sem os nomes. Fica em "Domina"; na 3ª, cobrar os três nomes de primeira. |
| 2026-10-06 | 1.1 | 1ª (1 dia de atraso) | Com uma pergunta de ajuda. Acertou entrada × saída, `default_factory` e que os erros voltam juntos num só `422`. Errou de primeira ao dizer que "a função roda"; corrigiu sozinho: a validação acontece antes. Fica em "Reconheço"; na 2ª, cobrar o "antes da função" de primeira. |
