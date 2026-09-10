# Lab — Técnicas de Pipelines (GitHub Actions)

> Repositório **template** da aula. Não faça fork — use **Use this template**.

Kit dos exercícios da aula: secrets e variáveis · condicionando pipelines · políticas de pipelines.

## Setup (5 min, antes do exercício 1)

1. Neste repositório, clique **Use this template → Create a new repository**. (NÃO faça fork: fork vem com Actions desligadas e os PRs apontam para o repositório do instrutor.)
2. Nome livre, dono = **sua conta**, visibilidade **Public** (Free só libera environments e rulesets em repo público). Create.
3. No seu repo novo: aba **Actions** → `00 - base` → *Run workflow* → precisa ficar **verde**. Se não rodou, avise antes de seguir.
4. Clone na sua máquina: `git clone https://github.com/SEU-USUARIO/SEU-REPO.git`
5. Você recebeu (em privado) dois tokens: `API_TOKEN` e `DEPLOY_TOKEN`. **Não commite, não cole no chat da turma.** Eles entram nos exercícios 3 e 4. A URL da API já está nos workflows.

Placar da turma (projetado na sala): `<API_URL>/placar`

## Exercícios

| # | Arquivo | Tema | Núcleo/Bônus |
|---|---|---|---|
| 1 | `.github/workflows/01-variaveis.yml` | env em 3 níveis, `vars`, contexto `github` | núcleo |
| 2 | `02-outputs.yml` | `GITHUB_OUTPUT`, `GITHUB_ENV`, outputs entre jobs | núcleo |
| 3 | `03-secrets.yml` | secret por `env`, deploy real em homolog, mascaramento | núcleo |
| 4 | `04-environment.yml` | environment, secret escopado, aprovação, deploy real em producao | núcleo |
| 5 | `05-condicoes.yml` | gatilhos, `paths`, `if`, `needs`, `failure()`, inputs | núcleo |
| 6 | `06-matrix.yml` | matrix, exclude/include, continue-on-error, concurrency | bônus |
| 7 | `07-politicas.yml` | ruleset na main, status check obrigatório | núcleo |
| 8 | `08-hardening.yml` | permissions mínimas, pin por SHA, pull_request_target | bônus |

Cada arquivo tem os `TODO` no próprio YAML. Gabarito em `exercicios/GABARITO.md` — abra só depois de tentar.

## Testes locais

```bash
python3 -m unittest discover -s app -v
```
